from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt6.QtCore import pyqtSignal, Qt
from app.ui.widgets.focusable import FocusableWidget


class SuggestionButton(FocusableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.word = ""

        self.label = QLabel("", self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("""
            font-size: 22px;
            color: white;
        """)

        self.setStyleSheet("""
            background-color: #444;
            border-radius: 10px;
        """)

        self.setMinimumHeight(70)

    def resizeEvent(self, event):
        self.label.setGeometry(self.rect())

    def set_word(self, word):
        self.word = word
        self.label.setText(word)

    def select(self):
        return self.word


class SuggestionBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QHBoxLayout()
        self.layout.setSpacing(15)
        self.setLayout(self.layout)

        self.buttons = []

        for _ in range(3):
            btn = SuggestionButton(self)
            btn.hide()
            self.layout.addWidget(btn)
            self.buttons.append(btn)

    def update_suggestions(self, suggestions):
        for i, btn in enumerate(self.buttons):
            if i < len(suggestions):
                btn.set_word(suggestions[i])
                btn.show()
            else:
                btn.hide()

    def get_focusables(self):
        return [btn for btn in self.buttons if btn.isVisible()]