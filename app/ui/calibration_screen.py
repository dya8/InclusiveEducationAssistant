'''from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from app.state.app_state import AppState

class CalibrationScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        layout = QVBoxLayout()
        layout.addWidget(QLabel("CALIBRATION SCREEN"))

        btn = QPushButton("Calibration Done")
        btn.clicked.connect(self.go_next)

        layout.addWidget(btn)
        self.setLayout(layout)

    def go_next(self):
        self.main_window.switch_state(AppState.HOME)

'''
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QPushButton, QProgressBar, QFrame
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPainter, QColor, QPen
from app.state.app_state import AppState


class CalibrationScreen(QWidget):
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
                stop:1 #e2e8f0
            );
            color: #0f172a;
            font-family: Inter;
        }

        QLabel#title {
            font-size: 24px;
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
            border-radius: 10px;
            font-size: 15px;
        }

        QPushButton:hover {
            background-color: #1d4ed8;
        }

        QPushButton:disabled {
            background-color: #93c5fd;
        }

        QProgressBar {
            height: 12px;
            background-color: #e5e7eb;
            border-radius: 6px;
        }

        QProgressBar::chunk {
            background-image: qlineargradient(
                x1:0, y1:0, x2:1, y2:0,
                stop:0 #2563eb,
                stop:1 #60a5fa
            );
            border-radius: 6px;
        }
        """)

        # ---------- CENTER PANEL ----------
        panel = QFrame()
        panel.setStyleSheet("""
        QFrame {
            background-color: rgba(255, 255, 255, 0.85);
            border-radius: 18px;
        }
        """)
        panel.setFixedWidth(420)

        panel_layout = QVBoxLayout(panel)
        panel_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        panel_layout.setSpacing(18)
        panel_layout.setContentsMargins(30, 30, 30, 30)

        title = QLabel("Calibration")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.subtitle = QLabel(
            "Please stay still while we adjust your settings."
        )
        self.subtitle.setObjectName("subtitle")
        self.subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.subtitle.setWordWrap(True)

        self.progress = QProgressBar()
        self.progress.setFixedWidth(260)
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self.progress.setTextVisible(False)

        self.btn = QPushButton("Finish Calibration")
        self.btn.setEnabled(False)
        self.btn.clicked.connect(self.go_next)

        panel_layout.addWidget(title)
        panel_layout.addWidget(self.subtitle)
        panel_layout.addSpacing(10)
        panel_layout.addWidget(self.progress)
        panel_layout.addSpacing(20)
        panel_layout.addWidget(self.btn)

        # ---------- ROOT LAYOUT ----------
        root = QVBoxLayout(self)
        root.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root.addWidget(panel)

        # ---------- TIMER ----------
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(45)

    # ---------- BACKGROUND GRID ----------
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        pen = QPen(QColor(203, 213, 225, 120))
        pen.setWidth(1)
        painter.setPen(pen)

        step = 40
        for x in range(0, self.width(), step):
            painter.drawLine(x, 0, x, self.height())

        for y in range(0, self.height(), step):
            painter.drawLine(0, y, self.width(), y)

    # ---------- LOGIC ----------
    def update_progress(self):
        self.progress_value += 1
        self.progress.setValue(self.progress_value)
        self.progress.update()

        if self.progress_value == 35:
            self.subtitle.setText("Measuring alignment…")
        elif self.progress_value == 70:
            self.subtitle.setText("Final adjustments in progress.")
        elif self.progress_value >= 100:
            self.timer.stop()
            self.subtitle.setText("Calibration complete.")
            self.btn.setEnabled(True)

    def go_next(self):
        self.main_window.switch_state(AppState.HOME)
