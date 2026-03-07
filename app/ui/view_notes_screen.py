from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QWidget
from PyQt6.QtCore import Qt
from app.ui.widgets.back_button import BackButton
from app.ui.widgets.note_item import NoteItem
from app.state.app_state import AppState
import os
from core.input.input_events import Action
from PyQt6.QtWidgets import QTextEdit
from app.ui.widgets.test_button import TestButton
from app.ui.widgets.delete_button import DeleteButton

class ViewNotesScreen(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(60,40,60,40)
        self.layout.setSpacing(20)

        title = QLabel("Saved Notes")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size:34px; font-weight:600;")
        self.layout.addWidget(title)

        self.back_button = BackButton(self)
        self.back_button.move(20,20)

        # scroll area
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        
        
        self.list_container = QWidget()
        self.list_layout = QVBoxLayout()
        self.list_layout.setSpacing(15)

        self.list_container.setLayout(self.list_layout)
        self.scroll.setWidget(self.list_container)

        self.layout.addWidget(self.scroll)
        self.viewer = QTextEdit()
        self.viewer.setReadOnly(True)
        self.viewer.setStyleSheet("font-size:28px")
        self.viewer.hide()
        self.layout.addWidget(self.viewer)

        self.delete_button = DeleteButton(self)
        self.delete_button.move(950,20)
        self.delete_button.hide()
        self.setLayout(self.layout)
        

        self.note_items = []
    # -------------------------------------------------
    # LOAD NOTES FOR CURRENT USER
    # -------------------------------------------------
    def load_notes(self):

        # clear old items
        for item in self.note_items:
            item.deleteLater()

        self.note_items = []

        user = AppState.current_user
        path = os.path.join("assets","notes",user)

        if not os.path.exists(path):
            return

        files = sorted(os.listdir(path), reverse=True)

        for f in files:

            item = NoteItem(f, path, self)

            self.list_layout.addWidget(item)

            self.note_items.append(item)
    
    def show_note(self, text,path):

        self.current_note_path = path
        self.scroll.hide()
        
        # show viewer
        self.viewer.setPlainText(text)
        self.viewer.show()
        self.delete_button.show()
        self.delete_button.raise_()
        

    def show_list(self):
        self.viewer.clear()
        self.viewer.hide()
        self.delete_button.hide()

        self.scroll.show()