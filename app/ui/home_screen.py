from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtCore import Qt
from app.ui.widgets.test_button import TestButton
from app.state.app_state import AppState
from core.input.input_events import Action

class HomeScreen(QWidget):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.main_window = main_window
        self.setFixedSize(1200, 800)
      

        # ---------- TITLE ----------
        title = QLabel("HOME", self)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 32px; font-weight: bold;")
        title.setGeometry(0, 40, 1200, 50)

        # ---------- TAKE NOTES ----------
        self.btn_notes = TestButton("TAKE NOTES", self)
        self.btn_notes.setObjectName("TakeNotes")
        self.btn_notes.resize(300, 120)
        self.btn_notes.move(450, 420)
        self.btn_notes.action = Action.OPEN_NOTES 

        # ---------- CODING ----------
        self.btn_coding = TestButton("CODING", self)
        self.btn_coding.setObjectName("Coding")
        self.btn_coding.resize(300, 120)
        self.btn_coding.move(450, 250)
        self.btn_coding.action = Action.OPEN_CODING
        
      

        # ---------- FOCUSABLES ----------
        self.focusables = [
            self.btn_notes,
            self.btn_coding
        ]
        
    def open_notes(self):
        self.main_window.switch_state(AppState.NOTES)
    def open_coding(self):
        print("CODING BUTTON SELECTED")   # 👈 ADD THIS
        self.main_window.switch_state(AppState.CODING)
        
        
