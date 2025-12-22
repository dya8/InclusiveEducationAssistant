from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtCore import Qt, QPoint


class EyeCursor(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.radius = 8
        self.pos = QPoint(400, 300)
        self.resize(self.radius * 2, self.radius * 2)
        self.move(self.pos)

    def set_position(self, x, y):
        self.pos = QPoint(int(x), int(y))
        self.move(self.pos)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QColor(0, 255, 0))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(0, 0, self.radius * 2, self.radius * 2)
