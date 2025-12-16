from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtCore import QPoint, QSize
from PyQt6.QtCore import Qt
class EyeCursor(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.radius = 8
        self.pos = QPoint(600, 400)  # start center
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.resize(parent.size())

    def move_cursor(self, dx, dy):
        self.pos.setX(max(0, min(self.width(), self.pos.x() + dx)))
        self.pos.setY(max(0, min(self.height(), self.pos.y() + dy)))
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setBrush(QColor(0, 255, 0))
        painter.setPen(QColor(0, 255, 0))
        painter.drawEllipse(self.pos, self.radius, self.radius)
    def pos(self):
        return self.geometry().center()
