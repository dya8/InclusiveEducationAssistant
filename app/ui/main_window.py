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
from app.ui.widgets.mic_button import MicButton
import os 
import cv2
from datetime import datetime
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
        # ---- LOGIN SIGNALS ----
        self.login_screen.login_success.connect(self.on_login_success)
        self.login_screen.new_user_detected.connect(self.on_new_user)
        self.keyboard_icon = KeyboardIcon(self)
        #self.keyboard_icon.move(900,500)
        #self.keyboard_icon.show()
        #self.keyboard_icon.raise_()

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

        
        # ---------------- INPUT ----------------
        self.input_manager = InputManager()
        self.cursor_controller = CursorController(self.eye_cursor)

        self.switch_state(AppState.LOGIN)

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

        self.CURSOR_GAIN_X = 0.10
        self.CURSOR_GAIN_Y = 0.05
        self.DEAD_RADIUS_X = 0.025
        self.DEAD_RADIUS_Y = 0.07

        # ---------------- TIMER ----------------
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_input)
        self.timer.start(30)

    # =====================================================
    def switch_state(self, state):
        # 🔥 Always clear focus properly
        if self.current_focus:
            self.current_focus.set_focus(False)

        self.current_focus = None
        self.dwell_manager.reset()
        self.input_manager.force_cursor_mode()
        #self.input_manager.reset()

        # 🔥 If leaving NOTES → fully clean its UI
        if self.current_state == AppState.NOTES:
            self.notes_screen.mic_button.hide()
            self.notes_screen.mic_label.hide()
            self.notes_screen.voice_active = False
            self.notes_screen.typing_active = False
            self.notes_screen.keyboard.hide()
            self.notes_screen.choice_overlay.hide()

        self.current_state = state

        # ===============================
        # LOGIN
        # ===============================
        if state == AppState.LOGIN:
            self.layout.setCurrentWidget(self.login_screen)
            return

        # ===============================
        # CALIBRATION
        # ===============================
        if state == AppState.CALIBRATION:
            self.layout.setCurrentWidget(self.calibration_screen)
            return

        # ===============================
        # HOME
        # ===============================
        if state == AppState.HOME:
            self.layout.setCurrentWidget(self.home_screen)
            self.focusables = list(self.home_screen.focusables)

            # 🔥 Critical: fresh list reference
            self.focusables = list(self.home_screen.focusables)
            return

        # ===============================
        # NOTES
        # ===============================
        if state == AppState.NOTES:
            self.layout.setCurrentWidget(self.notes_screen)

            self.notes_screen.choice_overlay.show()
            self.notes_screen.choice_overlay.raise_()

            self.focusables = (
                list(self.notes_screen.choice_overlay.focusables)
                + [self.notes_screen.back_button]
            )
            return


    '''def switch_state(self, state):
        if self.current_state == AppState.NOTES:
            self.notes_screen.mic_button.hide()
            self.notes_screen.voice_active = False

        self.current_state = state

        if state == AppState.LOGIN:
            self.layout.setCurrentWidget(self.login_screen)

        elif state == AppState.CALIBRATION:
            self.layout.setCurrentWidget(self.calibration_screen)

        elif state == AppState.HOME:
            self.layout.setCurrentWidget(self.home_screen)
            self.focusables = list(self.home_screen.focusables)
            self.current_focus = None

        elif state == AppState.NOTES:
            self.layout.setCurrentWidget(self.notes_screen)

            # 🔑 SHOW INPUT CHOICE IMMEDIATELY
            self.notes_screen.choice_overlay.show()
            self.notes_screen.choice_overlay.raise_()

            self.focusables = (
            list(self.notes_screen.choice_overlay.focusables)
            + [self.notes_screen.back_button]
            )

            self.current_focus = None
            self.dwell_manager.reset()
        self.input_manager.reset()'''
    def save_new_user_face(self, frame):
    # Create base directory if not exists

        base_dir = os.path.join("assets", "faces")
        os.makedirs(base_dir, exist_ok=True)

        # Determine next user_id
        existing_users = [
            d for d in os.listdir(base_dir)
            if d.startswith("user_")
        ]

        next_id = len(existing_users) + 1
        user_id = f"user_{next_id:03d}"

        user_dir = os.path.join(base_dir, user_id)
        os.makedirs(user_dir, exist_ok=True)

        # Save image
        filename = f"img1.jpg"
        filepath = os.path.join(user_dir, filename)

        cv2.imwrite(filepath, frame)

        print(f"[NEW USER] Saved face for {user_id} at {filepath}")

        return user_id
    
    def on_login_success(self, user_id):
        print(f"[MainWindow] Login successful: {user_id}")
         # Store user if needed
        AppState.current_user = user_id  # optional
        self.switch_state(AppState.CALIBRATION)
        self.calib_index = 0
        self.calib_start_time = None

    def on_new_user(self):
        print("New user detected")

        # Get current frame from login screen
        frame = self.login_screen.current_frame

        if frame is not None:
            user_id = self.save_new_user_face(frame)
            print("Registered new user:", user_id)
        else:
            print("Warning: No frame captured for new user")

        # Reset calibration state
        self.calib_index = 0
        self.calib_start_time = None

        # Move to calibration
        self.switch_state(AppState.CALIBRATION)
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
        if self.rotating_keyboard.isVisible() and self.rotating_keyboard.active:
            # Still process blink + actions, but DO NOT move cursor
            action = self.input_manager.update(
                gaze=None,
                blink=blink
            )

            # 🔑 FIX: normalize keyboard select
            if action == Action.KEYBOARD_SELECT:
                action = Action.SELECT

            self.handle_action(action)
            return


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
        self.update_focus()

        #print("RAW ACTION:", action)
        #print("CURRENT FOCUS:", type(self.current_focus))
        #THIS IS THE ONLY SELECTION LOGIC
        if action == Action.SELECT and self.current_focus:
           result = self.current_focus.select()
           self.handle_action(result)
           self.dwell_manager.reset()
           return
        
        self.handle_action(action)
        
    def restore_normal_input(self):
        if self.current_state == AppState.HOME:
            self.focusables = self.home_screen.focusables

        elif self.current_state == AppState.NOTES:

            # 🎤 VOICE MODE ACTIVE
            if self.notes_screen.mic_button.isVisible():
                self.focusables = [self.notes_screen.mic_button,self.notes_screen.back_button]

            # ⌨️ TYPING MODE ACTIVE
            elif self.notes_screen.typing_active:
                self.focusables = self.notes_screen.keyboard.focusables

            # 📋 CHOICE OVERLAY
            else:
                self.focusables = (
                    list(self.notes_screen.choice_overlay.focusables)
                    + [self.notes_screen.back_button]
                )

        self.current_focus = None
        self.dwell_manager.reset()


    # =====================================================

    def handle_action(self, action: Action):
        if action == Action.NONE:
            return
        # ==================================================
        # BACK BUTTON (GLOBAL)
        # ==================================================
        
        if action == Action.BACK:
            # Always clear current focus highlight first
            if self.current_focus:
                self.current_focus.set_focus(False)
            self.current_focus = None
            self.dwell_manager.reset()
            # 1️⃣ If rotating keyboard open → close it only
            if self.rotating_keyboard.isVisible():
                self.rotating_keyboard.close()
                self.input_manager.force_cursor_mode()
                #self.input_manager.reset()
                self.restore_normal_input()
                return

            # 2️⃣ If inside NOTES → handle internal navigation
            if self.current_state == AppState.NOTES:

                # Typing keyboard active → go back to choice overlay
                if self.notes_screen.typing_active:
                    self.notes_screen.keyboard.hide()
                    self.notes_screen.typing_active = False

                    self.notes_screen.choice_overlay.show()
                    self.notes_screen.choice_overlay.raise_()

                    self.focusables = (
                        list(self.notes_screen.choice_overlay.focusables)
                        + [self.notes_screen.back_button]
                    )
                    self.current_focus = None
                    self.input_manager.force_cursor_mode()
                    #self.input_manager.reset()
                    return

                # Voice input page → go back to choice overlay
                if self.notes_screen.mic_button.isVisible():
                    self.notes_screen.mic_button.hide()
                    self.notes_screen.mic_label.hide()
                    self.notes_screen.voice_active = False

                    self.notes_screen.choice_overlay.show()
                    self.notes_screen.choice_overlay.raise_()

                    self.focusables = (
                        list(self.notes_screen.choice_overlay.focusables)
                        + [self.notes_screen.back_button]
                    )
                    self.current_focus = None
                    self.input_manager.force_cursor_mode()
                    #self.input_manager.reset()
                    return

                # If already in choice overlay → go HOME
                if self.notes_screen.choice_overlay.isVisible():
                    self.switch_state(AppState.HOME)
                    self.input_manager.force_cursor_mode()
                    #self.input_manager.reset()
                    return
                
                return


        # ---------- ROTATING KEYBOARD (ABSOLUTE PRIORITY) ----------
        if self.rotating_keyboard.isVisible() :

            if action == Action.SELECT:
                result = self.rotating_keyboard.select_current()

                # 👇 THIS WAS THE MISSING PART
                if result == Action.CLOSE_KEYBOARD:
                    self.rotating_keyboard.close()
                    self.input_manager.force_cursor_mode()          # 🔑 REQUIRED
                    self.restore_normal_input()

                return

            if action == Action.BACK:
                #self.input_manager.last_action_time = time.time()
                self.rotating_keyboard.close()
                self.input_manager.force_cursor_mode()              # 🔑 REQUIRED
                self.restore_normal_input()
                return

            return  # swallow all actions
        
        # ==================================================
        # VOICE INPUT BLINK TOGGLE (START / STOP)
        # ==================================================
        if (
            action == Action.VOICE_TOGGLE
            and self.current_state == AppState.NOTES
        ):
            self.notes_screen.toggle_voice_input()
            return

        

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

        
        # ==================================================
        # HANDLE SELECT RESULTS (NO SELECTING HERE)
        # ==================================================

        if action == Action.OPEN_KEYBOARD:
            self.notes_screen.choice_overlay.hide()
            self.notes_screen.keyboard.show()
            self.notes_screen.typing_active = True
            self.focusables = self.notes_screen.keyboard.focusables
            self.current_focus = None
            self.dwell_manager.reset()
            return

        if action == Action.VOICE_INPUT:
            self.notes_screen.choice_overlay.hide()
            self.notes_screen.mic_button.show()
            self.notes_screen.mic_button.raise_()
            self.focusables = [self.notes_screen.mic_button,self.notes_screen.back_button]
            self.current_focus = None
            self.dwell_manager.reset()
            return
        if action == Action.OPEN_TYPING_KEYBOARD:
            self.notes_screen.choice_overlay.hide()
            self.notes_screen.keyboard.show()
            self.notes_screen.typing_active = True

            self.focusables = self.notes_screen.keyboard.focusables
            self.current_focus = None
            self.dwell_manager.reset()
            return


        # ---------- GENERIC SELECT HANDLER ----------
        if action == Action.SELECT and self.current_focus:
            result = self.current_focus.select()
            self.dwell_manager.reset()

            # 🔑 KEYBOARD OUTPUT (CHAR, SPACE, BACK, DONE)
            if (
                self.current_state == AppState.NOTES
                and self.notes_screen.typing_active
                and isinstance(action, tuple)
            ):
                kb_action, value = action
                self.notes_screen.handle_keyboard_action(kb_action, value)
                return

            # ---------- NORMAL ACTION ----------
            if action == Action.OPEN_NOTES:
                self.switch_state(AppState.NOTES)
                return

            action = result


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
            progress, _ = self.dwell_manager.update(hit)
            hit.update_dwell(progress)
