from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor, QPen, QFont
from PyQt6.QtCore import Qt, QPoint, QTimer
import math

from core.audio.tts import speak
from core.input.input_events import Action

from core.audio.tts import reset_tts
class RotatingKeyboard(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # ---- ACTIONS ----
        self.actions = ["HELP", "WATER", "TOILET", "PAIN", "YES", "NO", "BACK"]
        self.num_sectors = len(self.actions)
        self.selected_index = 0
        self.active = False

        # ---- ROTATION TIMER ----
        self.rotate_timer = QTimer(self)
        self.rotate_timer.timeout.connect(self.rotate)
        self.rotate_timer.start(2000)  # ms per action

        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.hide()

    # -------------------------
    # PUBLIC API
    # -------------------------

    def open(self):
        self.active =  True
        self.show()
        self.raise_()
        self.selected_index = 0
        self.parent().gaze_smoother.reset()

    def close(self):
        self.active = False
        self.hide()
        reset_tts()
        self.parent().gaze_smoother.reset()

    def rotate(self):
        if not self.isVisible() or not self.active:
            return

        self.selected_index = (self.selected_index + 1) % self.num_sectors
        self.update()

    def select_current(self):
        action = self.actions[self.selected_index]

        speak(action)   # 👈 ONLY HERE

        if action == "BACK":
            return Action.CLOSE_KEYBOARD

        print("COMM ACTION:", action)
        return Action.CLOSE_KEYBOARD


    # -------------------------
    # PAINT
    # -------------------------

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
                painter.setBrush(QColor(0, 180, 0, 180))
            else:
                painter.setBrush(QColor(180, 180, 180, 120))

            painter.setPen(QPen(Qt.GlobalColor.black, 2))
            painter.drawPie(
                cx - radius, cy - radius,
                radius * 2, radius * 2,
                start_angle * 16,
                span_angle * 16
            )

            mid_angle = math.radians(start_angle + sector_angle / 2)
            tx = cx + math.cos(mid_angle) * (radius - 50)
            ty = cy - math.sin(mid_angle) * (radius - 50)

            painter.setFont(QFont("Arial", 12, QFont.Weight.Bold))
            painter.setPen(Qt.GlobalColor.black)
            painter.drawText(QPoint(int(tx - 25), int(ty + 5)), label)
    

