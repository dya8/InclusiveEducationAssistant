from PyQt6.QtWidgets import QWidget, QVBoxLayout
from core.input.input_events import Action
from app.ui.coding.coding_keybutton import CodingKeyButton


class CodingTemplates(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # ===== TEMPLATE BUTTONS =====

        self.btn_if = CodingKeyButton(
            "if",
            Action.INSERT_TEMPLATE,
            "if :\n\t",
            self
        )

        self.btn_while = CodingKeyButton(
            "while",
            Action.INSERT_TEMPLATE,
            "while True:\n\t",
            self
        )

        self.btn_for = CodingKeyButton(
            "for",
            Action.INSERT_TEMPLATE,
            "for i in range():\n\t",
            self
        )

        self.btn_def = CodingKeyButton(
            "def",
            Action.INSERT_TEMPLATE,
            "def function():\n\t",
            self
        )

        self.btn_print = CodingKeyButton(
            "print()",
            Action.INSERT_TEMPLATE,
            "print()",
            self
        )

        # ===== BACK BUTTON =====

        self.btn_back = CodingKeyButton(
            "Back",
            Action.OPEN_MAIN,
            None,
            self
        )

        # ===== ADD TO LAYOUT =====

        layout.addWidget(self.btn_if)
        layout.addWidget(self.btn_while)
        layout.addWidget(self.btn_for)
        layout.addWidget(self.btn_def)
        layout.addWidget(self.btn_print)
        layout.addWidget(self.btn_back)

        # ===== FOCUSABLES =====

        self.focusables = [
            self.btn_if,
            self.btn_while,
            self.btn_for,
            self.btn_def,
            self.btn_print,
            self.btn_back
        ]