from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QStackedLayout
)
from app.state.app_state import AppState
from app.ui.login_screen import LoginScreen
from app.ui.calibration_screen import CalibrationScreen
from app.ui.home_screen import HomeScreen
from app.ui.widgets.eye_cursor import EyeCursor
from PyQt6.QtCore import QTimer
from core.input.input_manager import InputManager
from core.input.input_events import GazeDirection, BlinkType
from app.ui.cursor_controller import CursorController
from PyQt6.QtCore import Qt
from core.input.dwell_manager import DwellManager
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Assistive Eye App")
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet("""
            QMainWindow {
                background-color:black;
            }
        """)


        self.current_state = AppState.LOGIN

        self.container = QWidget()
        self.layout = QStackedLayout()

        self.login_screen = LoginScreen(self)
        self.calibration_screen = CalibrationScreen(self)
        self.home_screen = HomeScreen(self)
        self.focusables = self.home_screen.focusables
        self.layout.addWidget(self.login_screen)
        self.layout.addWidget(self.calibration_screen)
        self.layout.addWidget(self.home_screen)
        self.dwell_manager = DwellManager()
        self.current_focus = None

        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)
        self.eye_cursor = EyeCursor(self)
        self.eye_cursor.show()
        self.switch_state(AppState.LOGIN)
        self.input_manager = InputManager()
        self.cursor_controller = CursorController(self.eye_cursor)
        self.fake_gaze = GazeDirection.CENTER
        self.fake_blink = BlinkType.NONE
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_input)
        self.timer.start(50)  # 20 FPS

    def switch_state(self, state: AppState):
        self.current_state = state

        if state == AppState.LOGIN:
            self.layout.setCurrentWidget(self.login_screen)
        elif state == AppState.CALIBRATION:
            self.layout.setCurrentWidget(self.calibration_screen)
        elif state == AppState.HOME:
            self.layout.setCurrentWidget(self.home_screen)
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

    def update_input(self):
        
        action = self.input_manager.update(
            gaze=self.fake_gaze,
            blink=self.fake_blink,
            dwell_time=0,
            head_stable=True
        )

        # ---- CURSOR MOVEMENT ----
        if action:
            self.cursor_controller.handle_action(action)

        # ---- STEP 6.8: BLINK OVERRIDE ----
        if self.fake_blink == BlinkType.SINGLE and self.current_focus:
            self.current_focus.select()
            self.dwell_manager.reset()

        self.fake_blink = BlinkType.NONE

        # ---- DWELL-BASED SELECTION ----
        self.update_focus()


    def keyPressEvent(self, event):
        key = event.key()
        if key == 16777234:  # LEFT
            self.fake_gaze = GazeDirection.LEFT
        elif key == 16777236:  # RIGHT
            self.fake_gaze = GazeDirection.RIGHT
        elif key == 16777235:  # UP
            self.fake_gaze = GazeDirection.UP
        elif key == 16777237:  # DOWN
            self.fake_gaze = GazeDirection.DOWN
        elif key == 32:  # SPACE = blink
            self.fake_blink = BlinkType.SINGLE
    def keyReleaseEvent(self, event):
        self.fake_gaze = GazeDirection.CENTER


