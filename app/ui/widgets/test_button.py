from PyQt6.QtWidgets import QLabel
from app.ui.widgets.focusable import FocusableWidget
from core.input.input_events import Action
class TestButton(FocusableWidget):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.label = QLabel(text, self)
        self.label.move(20, 15)
        self.resize(160, 60)

    def select(self):
        if self.objectName() == "TakeNotes":
            print("Take Notes selected")
            return Action.OPEN_NOTES

        return Action.NONE



