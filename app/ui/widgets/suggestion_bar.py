from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PyQt6.QtCore import pyqtSignal


class SuggestionBar(QWidget):
    suggestion_selected = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QHBoxLayout()
        self.layout.setSpacing(15)
        self.setLayout(self.layout)

        self.buttons = []

        # Create 3 large suggestion buttons
        for _ in range(3):
            btn = QPushButton("")
            btn.setMinimumHeight(70)
            btn.setStyleSheet("""
                QPushButton {
                    font-size: 22px;
                    padding: 10px;
                    border-radius: 10px;
                    background-color: #444;
                    color: white;
                }
                QPushButton:hover {
                    background-color: #666;
                }
            """)
            btn.clicked.connect(self.handle_click)
            btn.hide()
            self.layout.addWidget(btn)
            self.buttons.append(btn)

    def update_suggestions(self, suggestions):
        """
        Updates the suggestion buttons.
        Expects a list of words (max 3).
        """
        for i, btn in enumerate(self.buttons):
            if i < len(suggestions):
                btn.setText(suggestions[i])
                btn.show()
            else:
                btn.hide()

    def handle_click(self):
        sender = self.sender()
        if sender:
            word = sender.text()
            self.suggestion_selected.emit(word)