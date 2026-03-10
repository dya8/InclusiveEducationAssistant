from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt
from app.ui.widgets.focusable import FocusableWidget

GROUPS = {
    "ABC": ["A", "B", "C"],
    "DEF": ["D", "E", "F"],
    "GHI": ["G", "H", "I"],
    "JKL": ["J", "K", "L"],
    "MNO": ["M", "N", "O"],
    "PQRS": ["P", "Q", "R", "S"],
    "TUV": ["T", "U", "V"],
    "WXYZ": ["W", "X", "Y", "Z"]
}

class KeyButton(FocusableWidget):
    def __init__(self, text, action, value=None, parent=None):
        super().__init__(parent)

        self.action = action
        self.value = value

        self.label = QLabel(text, self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        '''self.label.setStyleSheet(
            "font-size: 22px; border: 2px solid white;"
        )'''
        self.label.setStyleSheet("""
            font-size: 26px;
    font-weight: 500;
    border: 1px solid #c8c8c8;
    border-radius: 10px;
    background-color: white;
    color: #222;
        """)

        self.resize(200, 110)

    def select(self):
        return self.action, self.value
    