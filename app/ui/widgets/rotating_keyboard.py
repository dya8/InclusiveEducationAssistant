from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor, QPen, QFont
from PyQt6.QtCore import Qt, QPoint
import math

class RotatingKeyboard(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.actions = ["HELP", "WATER", "TOILET", "PAIN", "YES", "NO"]
        self.num_sectors = len(self.actions)
        self.selected_index = 0

        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.hide()

    def open(self):
        self.show()
        self.raise_()

    def close(self):
        self.hide()

    def rotate_left(self):
        self.selected_index = (self.selected_index - 1) % self.num_sectors
        self.update()

    def rotate_right(self):
        self.selected_index = (self.selected_index + 1) % self.num_sectors
        self.update()

    def get_selected_action(self):
        return self.actions[self.selected_index]

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w = self.width()
        h = self.height()
        cx, cy = w // 2, h // 2
        radius = min(cx, cy) - 80

        sector_angle = 360 / self.num_sectors

        for i, label in enumerate(self.actions):
            start_angle = int(i * sector_angle)
            span_angle = int(sector_angle)

            if i == self.selected_index:
                painter.setBrush(QColor(0, 200, 0, 180))
            else:
                painter.setBrush(QColor(200, 200, 200, 120))

            painter.setPen(QPen(Qt.GlobalColor.black, 2))
            painter.drawPie(
                cx - radius, cy - radius,
                radius * 2, radius * 2,
                start_angle * 16,
                span_angle * 16
            )

            # Draw label
            mid_angle = math.radians(start_angle + sector_angle / 2)
            tx = cx + math.cos(mid_angle) * (radius - 50)
            ty = cy - math.sin(mid_angle) * (radius - 50)

            painter.setPen(Qt.GlobalColor.black)
            painter.setFont(QFont("Arial", 12, QFont.Weight.Bold))
            painter.drawText(QPoint(int(tx - 25), int(ty + 5)), label)
