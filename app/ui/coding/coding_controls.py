from PyQt6.QtWidgets import QWidget, QVBoxLayout
from core.input.input_events import Action
from app.ui.coding.coding_keybutton import CodingKeyButton


class CodingControls(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.btn_backspace = CodingKeyButton(
            "Backspace",
            Action.BACKSPACE,
            None,
            self
        )

        self.btn_enter = CodingKeyButton(
            "Enter",
            Action.INSERT_CHAR,
            "\n",
            self
        )

        self.btn_space = CodingKeyButton(
            "Space",
            Action.INSERT_CHAR,
            " ",
            self
        )

        layout.addWidget(self.btn_backspace)
        layout.addWidget(self.btn_enter)
        layout.addWidget(self.btn_space)

        self.focusables = [
            self.btn_backspace,
            self.btn_enter,
            self.btn_space
        ]