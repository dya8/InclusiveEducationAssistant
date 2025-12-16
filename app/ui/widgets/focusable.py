from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtCore import QRect

class FocusableWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.focused = False
        self.dwell_progress = 0.0

    def set_focus(self, focused: bool):
        self.focused = focused
        if not focused:
            self.dwell_progress = 0.0
        self.update()

    def update_dwell(self, progress: float):
        self.dwell_progress = progress
        self.update()

    def select(self):
        print("SELECTED:", self.objectName())

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.focused:
            painter = QPainter(self)
            painter.setPen(QColor(0, 255, 0))
            painter.drawRect(self.rect().adjusted(1,1,-1,-1))
