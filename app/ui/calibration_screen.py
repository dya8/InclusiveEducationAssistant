from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor, QPen
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
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w = self.width()
        h = self.height()

        # -------- Background --------
        painter.fillRect(self.rect(), QColor(55, 55, 55))  # dark grey

        # -------- Grid Settings --------
        grid_spacing = 20  # distance between grid lines
        pen = QPen(QColor(90, 90, 90))  # light grey grid
        pen.setWidth(1)
        painter.setPen(pen)

        # Draw vertical lines
        for x in range(0, w, grid_spacing):
            painter.drawLine(x, 0, x, h)

        # Draw horizontal lines
        for y in range(0, h, grid_spacing):
            painter.drawLine(0, y, w, y)

        # -------- Draw Dot --------
        if self.dot_x is not None and self.dot_y is not None:
            cx = int(self.dot_x * w)
            cy = int(self.dot_y * h)

            painter.setBrush(QColor(255, 0, 0))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(cx - 10, cy - 10, 20, 20)