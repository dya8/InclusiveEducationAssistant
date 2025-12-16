from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
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
