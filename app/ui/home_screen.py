from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtCore import Qt
from app.ui.widgets.test_button import TestButton


class HomeScreen(QWidget):
    def __init__(self, main_window):
        super().__init__(main_window)
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
        self.btn_notes.move(450, 250)

        # ---------- CODING ----------
        self.btn_coding = TestButton("CODING", self)
        self.btn_coding.setObjectName("Coding")
        self.btn_coding.resize(300, 120)
        self.btn_coding.move(450, 420)

        # ---------- VIEW NOTES ----------
        self.btn_view_notes = TestButton("VIEW NOTES", self)
        self.btn_view_notes.setObjectName("ViewNotes")
        self.btn_view_notes.resize(300, 120)
        self.btn_view_notes.move(450, 590)

        # ---------- DWELL LABEL ----------
        self.dwell_label = QLabel("Dwell: 1.5 s", self)
        self.dwell_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.dwell_label.setStyleSheet("font-size:20px; font-weight:600;")
        self.dwell_label.setGeometry(950, 120, 200, 50)

        # ---------- DWELL + ----------
        self.btn_dwell_up = TestButton("Dwell up +", self)
        self.btn_dwell_up.setObjectName("DwellUp")
        self.btn_dwell_up.resize(100, 100)
        self.btn_dwell_up.move(950, 180)

        # ---------- DWELL - ----------
        self.btn_dwell_down = TestButton("Dwell down -", self)
        self.btn_dwell_down.setObjectName("DwellDown")
        self.btn_dwell_down.resize(100, 100)
        self.btn_dwell_down.move(1060, 180)

        # ---------- FOCUSABLES ----------
        self.focusables = [
            self.btn_notes,
            self.btn_coding,
            self.btn_view_notes,
            self.btn_dwell_down,
            self.btn_dwell_up
        ]
