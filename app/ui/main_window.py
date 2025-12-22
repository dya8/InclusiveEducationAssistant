from PyQt6.QtWidgets import QMainWindow, QWidget, QStackedLayout
from PyQt6.QtCore import QTimer, Qt
import time
from core.vision.gaze_smoother import GazeKalman

from app.state.app_state import AppState
from app.ui.login_screen import LoginScreen
from app.ui.calibration_screen import CalibrationScreen
from app.ui.home_screen import HomeScreen
from app.ui.widgets.eye_cursor import EyeCursor
from app.ui.widgets.rotating_keyboard import RotatingKeyboard
from app.ui.cursor_controller import CursorController

from core.input.input_events import Action, BlinkType
from core.input.input_manager import InputManager
from core.input.dwell_manager import DwellManager

from core.vision.camera import CameraManager
from core.vision.face_mesh import FaceMeshDetector
from core.vision.blink_detector import BlinkDetector
from core.vision.gaze_estimator import GazeEstimator
from core.vision.gaze_calibration import GazeCalibration


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Assistive Eye App")
        self.setGeometry(100, 100, 1200, 800)

        self.current_state = AppState.LOGIN

        # ---------------- UI ----------------
        self.container = QWidget()
        self.layout = QStackedLayout()

        self.login_screen = LoginScreen(self)
        self.calibration_screen = CalibrationScreen(self)
        self.home_screen = HomeScreen(self)

        self.focusables = self.home_screen.focusables
        self.current_focus = None
        self.dwell_manager = DwellManager()

        self.layout.addWidget(self.login_screen)
        self.layout.addWidget(self.calibration_screen)
        self.layout.addWidget(self.home_screen)

        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)

        self.eye_cursor = EyeCursor(self)
        self.eye_cursor.show()

        self.rotating_keyboard = RotatingKeyboard(self)
        self.rotating_keyboard.setGeometry(0, 0, self.width(), self.height())
        self.gaze_smoother = GazeKalman()

        self.switch_state(AppState.LOGIN)

        # ---------------- INPUT ----------------
        self.input_manager = InputManager()
        self.cursor_controller = CursorController(self.eye_cursor)

        # ---------------- CAMERA & VISION ----------------
        self.camera = CameraManager()
        self.camera.start()

        self.face_mesh = FaceMeshDetector()
        self.blink_detector = BlinkDetector()
        self.gaze_estimator = GazeEstimator()
        self.gaze_calibration = GazeCalibration()

        self.real_blink = BlinkType.NONE

        # ---------------- CALIBRATION ----------------
        self.calibration_points = [
            ("CENTER", 0.5, 0.5),
            ("LEFT", 0.1, 0.5),
            ("RIGHT", 0.9, 0.5),
            ("UP", 0.5, 0.1),
            ("DOWN", 0.5, 0.9),
        ]
        self.calib_index = 0
        self.calib_start_time = None
        self.CALIB_SETTLE = 0.3
        self.CALIB_COLLECT = 1.2

        # ---------------- TIMER ----------------
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_input)
        self.timer.start(30)

    # =====================================================

    def switch_state(self, state):
        self.current_state = state
        if state == AppState.LOGIN:
            self.layout.setCurrentWidget(self.login_screen)
        elif state == AppState.CALIBRATION:
            self.layout.setCurrentWidget(self.calibration_screen)
        elif state == AppState.HOME:
            self.layout.setCurrentWidget(self.home_screen)

    # =====================================================

    def update_input(self):
        frame = self.camera.get_frame()
        if frame is None:
            return

        eyes = self.face_mesh.get_eye_landmarks(frame)
        if not eyes:
            return

        self.real_blink = self.blink_detector.update(
            eyes["left_eye"],
            eyes["right_eye"]
        )

        gx, gy = self.gaze_estimator.estimate(
            eyes["left_eye"],
            eyes["right_eye"],
            eyes["left_iris"],
            eyes["right_iris"]
        )

        # ---------------- CALIBRATION MODE ----------------
        if self.current_state == AppState.CALIBRATION:
            label, x, y = self.calibration_points[self.calib_index]

            if self.calib_start_time is None:
                self.calib_start_time = time.time()
                self.calibration_screen.show_dot(x, y)

            elapsed = time.time() - self.calib_start_time

            if self.CALIB_SETTLE < elapsed < self.CALIB_COLLECT:
                self.gaze_calibration.add_sample(label, gx, gy)

            if elapsed >= self.CALIB_COLLECT:
                self.calib_index += 1
                self.calib_start_time = None

                if self.calib_index >= len(self.calibration_points):
                    self.gaze_calibration.finalize()
                    self.switch_state(AppState.HOME)
            return

        mapped = self.gaze_calibration.map(gx, gy)
        if mapped:
            cx, cy = mapped

            # ---- KALMAN SMOOTHING ----
            sx, sy = self.gaze_smoother.smooth(cx, cy)

            self.cursor_controller.move_to(sx, sy)


        # ---------------- BLINK SELECT ----------------
        if self.real_blink == BlinkType.SINGLE and self.current_focus:
            self.current_focus.select()
            self.dwell_manager.reset()

        self.update_focus()

    # =====================================================

    def update_focus(self):
        cursor_pos = self.eye_cursor.pos
        hit = None

        for w in self.focusables:
            if w.geometry().contains(cursor_pos):
                hit = w
                break

        if hit != self.current_focus:
            if self.current_focus:
                self.current_focus.set_focus(False)
            self.current_focus = hit
            if hit:
                hit.set_focus(True)
            self.dwell_manager.reset()

        if hit:
            progress, selected = self.dwell_manager.update(hit)
            hit.update_dwell(progress)
            if selected:
                hit.select()
                self.dwell_manager.reset()
