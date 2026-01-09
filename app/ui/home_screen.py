'''from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from app.ui.widgets.test_button import TestButton


class HomeScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()

        layout = QVBoxLayout()
        layout.addWidget(QLabel("HOME SCREEN"))
        layout.addWidget(QLabel("• Take Notes"))
        layout.addWidget(QLabel("• Coding"))
        layout.addWidget(QLabel("• View Materials"))
        self.btn1 = TestButton("Take Notes", self)
        self.btn1.move(100, 100)
        self.btn1.setObjectName("TakeNotes")

        self.btn2 = TestButton("Coding", self)
        self.btn2.move(100, 200)
        self.btn2.setObjectName("Coding")
        self.focusables = [self.btn1, self.btn2]
        self.setLayout(layout)
'''
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QColor, QLinearGradient
from app.ui.widgets.test_button import TestButton


class HomeScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        # ---------- GLOBAL STYLE ----------
        self.setStyleSheet("""
        QWidget {
           
            color: #e5e7eb;
            font-family: Inter;
        }

        QLabel#AppTitle {
            font-size: 22px;
            font-weight: 600;
            color: #e5e7eb;
        }

        QLabel#SectionTitle {
            font-size: 16px;
            font-weight: 500;
            color: #c7d2fe;
        }

        QFrame#Header {
            background: qlineargradient(
                x1:0, y1:0, x2:1, y2:0,
                stop:0 #020617,
                stop:1 #0f172a
            );
        }

        QFrame#Sidebar {
            background-color: rgba(30, 41, 59, 0.7);
            border-radius: 18px;
        }

        QFrame#MainArea {
            background: qlineargradient(
                x1:0, y1:0, x2:1, y2:1,
                stop:0 #020617,
                stop:1 #0f172a
            );
            border-radius: 22px;
        }
        """)

        # ---------- ROOT ----------
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ---------- HEADER ----------
        header = QFrame()
        header.setObjectName("Header")
        header.setFixedHeight(70)

        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(24, 10, 24, 10)
        header_layout.setSpacing(20)

        title = QLabel("EyeLearn")
        title.setObjectName("AppTitle")

        header_layout.addWidget(title)
        header_layout.addStretch()

        

        root.addWidget(header)

        # ---------- BODY ----------
        body = QHBoxLayout()
        body.setContentsMargins(20, 20, 20, 20)
        body.setSpacing(20)

        # ---------- SIDEBAR ----------
        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(200)

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(20, 20, 20, 20)
        sidebar_layout.setSpacing(16)
        sidebar_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        quick = QLabel("Quick Access")
        quick.setObjectName("SectionTitle")

        sidebar_layout.addWidget(quick)

        for text in ["📒 Notes", "💻 Coding", "📑 PPT", "🧑‍🏫 Ask Teacher"]:
            btn = TestButton(text, self)
            btn.setFixedHeight(40)
            btn.setStyleSheet("""
            QPushButton {
               
                color: #e5e7eb;
                
            }
            
            """)
            sidebar_layout.addWidget(btn)

        sidebar_layout.addStretch()

        # ---------- MAIN CONTENT ----------
        main_area = QFrame()
        main_area.setObjectName("MainArea")

        main_layout = QVBoxLayout(main_area)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(16)

        content_label = QLabel("Content Area")
        content_label.setObjectName("SectionTitle")

        main_layout.addWidget(content_label)
        main_layout.addStretch()

        # ---------- ASSEMBLE ----------
        body.addWidget(sidebar)
        body.addWidget(main_area, stretch=1)
        root.addLayout(body)

        # ---------- FOCUSABLES ----------
        self.focusables = self.findChildren(TestButton)

    # ---------- SUBTLE BACKGROUND ACCENT ----------
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        grad = QLinearGradient(0, 0, self.width(), self.height())
        grad.setColorAt(0, QColor(59, 130, 246, 25))
        grad.setColorAt(1, QColor(34, 197, 94, 20))

        painter.fillRect(self.rect(), grad)
