'''from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from app.state.app_state import AppState

class LoginScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        layout = QVBoxLayout()

        layout.addWidget(QLabel("LOGIN SCREEN"))
        btn = QPushButton("Simulate Login")
        btn.clicked.connect(self.go_next)

        layout.addWidget(btn)
        self.setLayout(layout)

    def go_next(self):
        self.main_window.switch_state(AppState.CALIBRATION)
'''
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QPushButton, QProgressBar
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPainter, QColor
from app.state.app_state import AppState


class LoginScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.progress_value = 0

        # ---------- STYLES ----------
        self.setStyleSheet("""
        QWidget {
            background-color: #f8fafc;
            background-image: qlineargradient(
                x1:0, y1:0, x2:0, y2:1,
                stop:0 #f8fafc,
                stop:1 #e0f2fe
            );
            color: #0f172a;
            font-family: Inter;
        }

        QLabel#title {
            font-size: 26px;
            font-weight: 600;
        }

        QLabel#subtitle {
            font-size: 15px;
            color: #475569;
        }

        QPushButton {
            background-color: #2563eb;
            color: white;
            border: none;
            padding: 14px 28px;
            border-radius: 12px;
            font-size: 15px;
        }

        QPushButton:hover {
            background-color: #1d4ed8;
        }

        QPushButton:disabled {
            background-color: #93c5fd;
        }
        """)

        # ---------- LAYOUT ----------
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(18)

        title = QLabel("Welcome")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.subtitle = QLabel(
            "We’re setting things up for a comfortable experience."
        )
        self.subtitle.setObjectName("subtitle")
        self.subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.subtitle.setWordWrap(True)

        # ✅ CREATE PROGRESS BAR FIRST
        self.progress = QProgressBar()
        self.progress.setFixedWidth(260)
        self.progress.setFixedHeight(14)
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self.progress.setTextVisible(False)

        # ✅ STYLE PROGRESS BAR
        self.progress.setStyleSheet("""
        QProgressBar {
            background-color: #e5e7eb;
            border-radius: 7px;
        }

        QProgressBar::chunk {
            background-color: qlineargradient(
                x1:0, y1:0, x2:1, y2:0,
                stop:0 #1d4ed8,
                stop:0.5 #3b82f6,
                stop:1 #60a5fa
            );
            border-radius: 7px;
        }
        """)

        self.btn = QPushButton("Continue")
        self.btn.setEnabled(False)
        self.btn.clicked.connect(self.go_next)

        layout.addWidget(title)
        layout.addWidget(self.subtitle)
        layout.addSpacing(10)
        layout.addWidget(self.progress, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(20)
        layout.addWidget(self.btn, alignment=Qt.AlignmentFlag.AlignCenter)

        # ---------- TIMER ----------
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(40)

    # ---------- BACKGROUND PAINT ----------
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)

        painter.setBrush(QColor(37, 99, 235, 35))
        painter.drawEllipse(
            self.width() // 2 - 280,
            self.height() // 2 - 200,
            560,
            400
        )

        painter.setBrush(QColor(59, 130, 246, 70))
        painter.drawEllipse(
            self.width() // 2 - 250,
            self.height() // 2 - 180,
            500,
            360
        )

        painter.setBrush(QColor(34, 197, 94, 45))
        painter.drawEllipse(
            self.width() // 2 - 180,
            self.height() // 2 + 90,
            360,
            240
        )

    # ---------- LOGIC ----------
    def update_progress(self):
        self.progress_value += 1
        self.progress.setValue(self.progress_value)
        self.progress.update()  # force repaint

        if self.progress_value == 40:
            self.subtitle.setText("Adjusting settings to suit your needs…")
        elif self.progress_value == 80:
            self.subtitle.setText("Almost ready.")
        elif self.progress_value >= 100:
            self.timer.stop()
            self.btn.setEnabled(True)
            self.subtitle.setText("You’re all set.")

    def go_next(self):
        self.main_window.switch_state(AppState.CALIBRATION)
