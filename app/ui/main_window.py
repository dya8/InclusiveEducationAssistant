from PyQt6.QtWidgets import QMainWindow, QWidget, QStackedLayout
from PyQt6.QtCore import QTimer
import time
from app.ui.notes_screen import NotesScreen
from PyQt6.QtCore import QRect
from core.vision.gaze_smoother import GazeKalman
from app.state.app_state import AppState
from app.ui.login_screen import LoginScreen
from app.ui.calibration_screen import CalibrationScreen
from app.ui.home_screen import HomeScreen
from app.ui.widgets.eye_cursor import EyeCursor
from app.ui.widgets.rotating_keyboard import RotatingKeyboard
from app.ui.cursor_controller import CursorController
from app.ui.widgets.keyboard_icon import KeyboardIcon
from core.input.input_events import Action, BlinkType
from core.input.input_manager import InputManager
from core.input.dwell_manager import DwellManager

from core.vision.camera import CameraManager
from core.vision.face_mesh import FaceMeshDetector
from core.vision.blink_detector import BlinkDetector
from core.vision.gaze_estimator import GazeEstimator
from core.vision.gaze_calibration import GazeCalibration
from core.ml.eye_state_cnn import EyeStateCNN


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
        self.keyboard_icon = KeyboardIcon(self)
        self.keyboard_icon.move(900,500)
        self.keyboard_icon.show()

        self.keyboard_icon.raise_()

        self.focusables = self.home_screen.focusables
        self.focusables.append(self.keyboard_icon)
        self.current_focus = None
        self.dwell_manager = DwellManager()

        self.layout.addWidget(self.login_screen)
        self.layout.addWidget(self.calibration_screen)
        self.layout.addWidget(self.home_screen)
        self.notes_screen = NotesScreen(self)
        self.layout.addWidget(self.notes_screen)

        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)

        self.eye_cursor = EyeCursor(self)
        self.eye_cursor.show()

        self.rotating_keyboard = RotatingKeyboard(self)
        self.rotating_keyboard.setGeometry(0, 0, self.width(), self.height())

        self.switch_state(AppState.LOGIN)

        # ---------------- INPUT ----------------
        self.input_manager = InputManager()
        self.cursor_controller = CursorController(self.eye_cursor)

        # ---------------- CAMERA & VISION ----------------
        self.camera = CameraManager()
        self.camera.start()

        self.face_mesh = FaceMeshDetector()

        self.eye_cnn = EyeStateCNN(
            "assets/models/eye_closed_model.keras"
        )
        self.blink_detector = BlinkDetector(self.eye_cnn)

        self.gaze_estimator = GazeEstimator()
        self.gaze_calibration = GazeCalibration()
        self.gaze_smoother = GazeKalman()

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
        self.CALIB_SETTLE = 0.5
        self.CALIB_COLLECT = 2.0

        self.cursor_x = 0.5
        self.cursor_y = 0.5

        self.CURSOR_GAIN_X = 0.14
        self.CURSOR_GAIN_Y = 0.07
        self.DEAD_RADIUS_X = 0.025
        self.DEAD_RADIUS_Y = 0.07

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
            self.focusables = self.home_screen.focusables
            self.current_focus = None

        elif state == AppState.NOTES:
            self.layout.setCurrentWidget(self.notes_screen)

            # 🔑 SHOW INPUT CHOICE IMMEDIATELY
            self.notes_screen.choice_overlay.show()
            self.notes_screen.choice_overlay.raise_()

            self.focusables = self.notes_screen.choice_overlay.focusables
            self.current_focus = None
            self.dwell_manager.reset()




    # =====================================================

    def update_input(self):
        frame = self.camera.get_frame()
        if frame is None:
            return

        eyes = self.face_mesh.get_eye_landmarks(frame)
        if not eyes:
            return

        # ---------- BLINK ----------
        blink = self.blink_detector.update(
            eyes["left_eye_img"],
            eyes["right_eye_img"],
            eyes["left_eye"],
            eyes["right_eye"]
        )

        # ---------- GAZE ----------
        gx, gy = self.gaze_estimator.estimate(
            eyes["left_eye"],
            eyes["right_eye"],
            eyes["left_iris"],
            eyes["right_iris"]
        )

        # ---------- CALIBRATION ----------
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
                    self.cursor_x = self.gaze_calibration.center_screen_x
                    self.cursor_y = self.gaze_calibration.center_screen_y
                    self.switch_state(AppState.HOME)
                return
        # ---------- FREEZE CURSOR WHEN KEYBOARD IS OPEN ----------
        if self.rotating_keyboard.isVisible():
            # Still process blink + actions, but DO NOT move cursor
            action = self.input_manager.update(
                gaze=None,
                blink=blink
            )

            # 🔑 FIX: normalize keyboard select
            if action == Action.KEYBOARD_SELECT:
                action = Action.SELECT

            self.handle_action(action)


        # ---------- CURSOR ----------
        mapped = self.gaze_calibration.map(gx, gy)
        if mapped is None:
            return

        cx, cy = mapped
        dx = cx - self.gaze_calibration.center_screen_x
        dy = cy - self.gaze_calibration.center_screen_y
        if abs(dx) < self.DEAD_RADIUS_X:
            cx = self.gaze_calibration.center_screen_x
        if abs(dy) < self.DEAD_RADIUS_Y:
            cy = self.gaze_calibration.center_screen_y


        

        dx_s, dy_s = self.gaze_smoother.smooth(
            cx - self.cursor_x,
            cy - self.cursor_y
        )

        self.cursor_x += dx_s * self.CURSOR_GAIN_X
        self.cursor_y += dy_s * self.CURSOR_GAIN_Y

        self.cursor_controller.move_to(self.cursor_x, self.cursor_y)


        # ---------- ACTION ----------
        action = self.input_manager.update(
            gaze=None,     # gaze actions come later
            blink=blink
        )

        # DEBUG (remove after verification)
        print("ACTION:", action)

        self.handle_action(action)
        self.update_focus()
        

    # =====================================================

    def handle_action(self, action: Action):
        if action == Action.NONE:
            return

        # ---------- ROTATING KEYBOARD (ABSOLUTE PRIORITY) ----------
        if self.rotating_keyboard.isVisible():

            if action == Action.SELECT:
                result = self.rotating_keyboard.select_current()
                self.input_manager.last_action_time = time.time()

                # 👇 THIS WAS THE MISSING PART
                if result == Action.CLOSE_KEYBOARD:
                    self.rotating_keyboard.close()

                return

            if action == Action.BACK:
                self.input_manager.last_action_time = time.time()
                self.rotating_keyboard.close()
                return

            return  # swallow all actions


        # ---------- GLOBAL LONG-BLINK ----------
        if action == Action.OPEN_KEYBOARD:
            self.input_manager.last_action_time = time.time()
            self.rotating_keyboard.open()
            return

        # ---------- OPEN NOTES ----------
        if action == Action.OPEN_NOTES:
            self.switch_state(AppState.NOTES)
            self.dwell_manager.reset()
            return

        # ---------- INPUT CHOICE OVERLAY ----------
        if (
            action == Action.SELECT
            and self.current_state == AppState.NOTES
            and self.notes_screen.choice_overlay.isVisible()
            and self.current_focus
        ):
            result = self.current_focus.select()
            self.dwell_manager.reset()

            if result == Action.OPEN_KEYBOARD:
                self.notes_screen.choice_overlay.hide()
                self.notes_screen.keyboard.show()
                self.notes_screen.typing_active = True
                self.focusables = self.notes_screen.keyboard.focusables
                self.current_focus = None
                return

            if result == Action.VOICE_INPUT:
                self.notes_screen.choice_overlay.hide()
                self.notes_screen.start_voice_input()
                print("VOICE INPUT SELECTED")
                return

        # ---------- NORMAL UI ----------
        if action == Action.SELECT and self.current_focus:
            result = self.current_focus.select()
            self.dwell_manager.reset()

            if result == Action.OPEN_NOTES:
                self.switch_state(AppState.NOTES)
                return


    # =====================================================

    def update_focus(self):
        cursor_pos = self.eye_cursor.pos
        hit = None

        for w in self.focusables:
            global_rect = QRect(
                w.mapToGlobal(w.rect().topLeft()),
                w.size()
            )

            if global_rect.contains(cursor_pos):
                hit = w
                break   # 🔴 THIS WAS MISSING

        if hit != self.current_focus:
            if self.current_focus:
                self.current_focus.set_focus(False)
            self.current_focus = hit
            if hit:
                hit.set_focus(True)
            self.dwell_manager.reset()

        if hit and not isinstance(hit, KeyboardIcon):
            progress, selected = self.dwell_manager.update(hit)
            hit.update_dwell(progress)
            if selected:
                hit.select()
                self.dwell_manager.reset()
