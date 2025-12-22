from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtCore import Qt


class CalibrationScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.dot_x = None  # normalized [0,1]
        self.dot_y = None  # normalized [0,1]

    def show_dot(self, x_norm, y_norm):
        """
        x_norm, y_norm ∈ [0,1]
        """
        self.dot_x = x_norm
        self.dot_y = y_norm
        self.update()

    def paintEvent(self, event):
        if self.dot_x is None or self.dot_y is None:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w = self.width()
        h = self.height()

        cx = int(self.dot_x * w)
        cy = int(self.dot_y * h)

        painter.setBrush(QColor(255, 0, 0))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(cx - 10, cy - 10, 20, 20)
