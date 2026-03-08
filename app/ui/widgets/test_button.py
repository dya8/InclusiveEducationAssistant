'''from PyQt6.QtWidgets import QLabel
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

        return Action.NONE'''

       
from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt
from app.ui.widgets.focusable import FocusableWidget
from core.input.input_events import Action


class TestButton(FocusableWidget):
    def __init__(self, text, parent=None):
        super().__init__(parent)

        # Default action
        self.action = Action.NONE

        # Force proper size so layout cannot shrink it too much
        self.setMinimumSize(200, 70)

        # Button styling (so it doesn't blend into dark background)
        self.setStyleSheet("""
            background-color: #2d2d2d;
            border: 2px solid #555;
            border-radius: 8px;
        """)

        # Centered label
        self.label = QLabel(text, self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("color: white; font-size: 16px;")
        self.label.setGeometry(0, 0, 200, 70)

    def select(self):
         return getattr(self, "action", Action.NONE)
    def mousePressEvent(self, event):
        if self.parent() and hasattr(self.parent(), "main_window"):
            action = self.select()
            self.parent().main_window.handle_action(action)
    


