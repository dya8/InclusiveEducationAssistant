from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout
from core.input.input_events import Action
from app.ui.widgets.focusable import FocusableWidget
import os


class NoteItem(FocusableWidget):

    def __init__(self, filename, folder, parent=None):
        super().__init__(parent)

        self.filename = filename
        self.path = os.path.join(folder, filename)

        layout = QHBoxLayout()

        self.label = QLabel(filename)
        self.label.setStyleSheet("font-size:28px")

        layout.addWidget(self.label)

        self.setLayout(layout)
        self.setMinimumHeight(100)

    def select(self):
        print("NOTE SELECTED:", self.filename)
        return ("OPEN_NOTE", self.path)
    
    '''def long_select(self):
        return ("DELETE_NOTE", self.path)'''