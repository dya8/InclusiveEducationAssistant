from PyQt6.QtWidgets import QLabel
from app.ui.widgets.focusable import FocusableWidget

class TestButton(FocusableWidget):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.label = QLabel(text, self)
        self.label.move(20, 15)
        self.resize(160, 60)

    def select(self):
        print(f"Button '{self.label.text()}' selected")
