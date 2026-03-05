from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit
from PyQt6.QtCore import Qt
import os

from app.state.app_state import AppState
from app.ui.widgets.back_button import BackButton


class ViewNotesScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout()

        title = QLabel("View Notes")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            font-size: 32px;
            font-weight: bold;
        """)

        layout.addWidget(title)

        # ---------- NOTES DISPLAY ----------
        self.notes_area = QTextEdit()
        self.notes_area.setReadOnly(True)
        self.notes_area.setStyleSheet("""
            font-size: 24px;
            padding: 20px;
        """)

        layout.addWidget(self.notes_area)

        self.setLayout(layout)

        self.back_button = BackButton(self)
        self.back_button.move(20, 20)
        self.back_button.show()
    # -------------------------------------------------
    # LOAD NOTES FOR CURRENT USER
    # -------------------------------------------------
    def load_notes(self):

        user_id = AppState.current_user
        base_dir = os.path.join("assets", "notes", user_id)

        if not os.path.exists(base_dir):
            self.notes_area.setPlainText("No notes found.")
            return

        notes_text = ""

        for file in sorted(os.listdir(base_dir)):
            filepath = os.path.join(base_dir, file)

            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            notes_text += f"\n----- {file} -----\n"
            notes_text += content + "\n"

        self.notes_area.setPlainText(notes_text)