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
        self.label.setStyleSheet(
            "font-size: 22px; border: 2px solid white;"
        )
        self.setStyleSheet("""
border: 2px solid white;
font-size: 26px;
padding: 10px;
""")

        self.resize(500, 600)

    def select(self):
        return self.action, self.value
    def mousePressEvent(self, event):

        result = self.select()

        parent = self.parent()
        while parent:
            if hasattr(parent, "main_window"):
                parent.main_window.handle_action(result)
                break
            parent = parent.parent()
    def set_focus(self, focused):

        if focused:
            self.setStyleSheet("""
            border: 3px solid #00ff00;
            background-color: rgba(0,255,0,40);
            color: white;
            font-size: 22px;
            """)
        else:
            self.setStyleSheet("""
            border: 2px solid white;
            background-color: rgba(0,0,0,0);
            color: white;
            font-size: 22px;
            """)