from PyQt6.QtWidgets import QWidget, QGridLayout
from app.ui.widgets.focusable import FocusableWidget
from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt
class KeyButton(FocusableWidget):
    def __init__(self, label, parent=None):
        super().__init__(parent)
        self.value = label

        self.text = QLabel(label, self)
        self.text.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.resize(70, 70)

    def select(self):
        return self.value

class TypingKeyboard(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QGridLayout()
        self.keys = []
        self.focusables = []

        rows = [
            list("QWERTYUIOP"),
            list("ASDFGHJKL"),
            list("ZXCVBNM"),
            ["SPACE", "BACKSPACE", "ENTER"]
        ]

        for r, row in enumerate(rows):
            for c, key in enumerate(row):
                btn = KeyButton(key, self)
                self.layout.addWidget(btn, r, c)
                self.keys.append(btn)
                self.focusables.append(btn)

        self.setLayout(self.layout)
