from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QGridLayout
from PyQt6.QtCore import Qt
from app.ui.widgets.test_button import TestButton


class HomeScreen(QWidget):
    def __init__(self, main_window):
        super().__init__(main_window)
        # Premium dark gradient background
        self.setStyleSheet("""
            QWidget#HomeScreen {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                                  stop:0 #0f172a, stop:1 #1e1b4b);
            }
        """)
        self.setObjectName("HomeScreen")
        self.setAutoFillBackground(True)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 60, 40, 60)
        main_layout.setSpacing(50)

        # ---------------- HOME TITLE ----------------
        self.title = QLabel("Assistive Hub", self)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet("""
            font-family: 'Outfit', 'Segoe UI', sans-serif;
            font-size: 56px;
            font-weight: 900;
            color: #f8fafc;
            letter-spacing: 4px;
        """)
        main_layout.addWidget(self.title)

        # ---------------- CARDS LAYOUT ----------------
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(40)
        cards_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.btn_coding, coding_card = self.create_card("Coding\nPlatform", "Coding", "#38bdf8", cards_layout)
        self.btn_view_notes, view_notes_card = self.create_card("View\nNotes", "ViewNotes", "#c084fc", cards_layout)
        self.btn_notes, notes_card = self.create_card("Note\nTaking", "TakeNotes", "#34d399", cards_layout)

        main_layout.addLayout(cards_layout)

        # Let cards push to center
        main_layout.addStretch()

        # ---------------- FOCUSABLES ----------------
        self.focusables = [
            self.btn_coding,
            self.btn_view_notes,
            self.btn_notes
        ]

    def create_card(self, title_text, obj_name, color, parent_layout):
        container = QWidget()
        container.setFixedSize(300, 400)
        
        # Grid layout to stack the visual card and the transparent button
        grid = QGridLayout(container)
        grid.setContentsMargins(0, 0, 0, 0)
        
        card = QWidget()
        card.setObjectName("AppCard")
        card.setStyleSheet(f"""
            QWidget#AppCard {{
                background-color: rgba(30, 41, 59, 180);
                border-radius: 28px;
                border: 2px solid rgba(255, 255, 255, 0.06);
            }}
            QWidget#AppCard:hover {{
                background-color: rgba(45, 55, 72, 220);
                border: 2px solid {color};
            }}
        """)
        
        card_layout = QVBoxLayout(card)
        card_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        title = QLabel(title_text)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(f"""
            font-family: 'Outfit', 'Segoe UI', sans-serif;
            font-size: 38px;
            font-weight: 800;
            color: {color};
            background: transparent;
            border: none;
        """)
        card_layout.addWidget(title)
        
        btn = TestButton("", container)
        btn.setObjectName(obj_name)
        # Transparent background for the button, so it doesn't hide the card
        btn.setStyleSheet("background: transparent; border: none;")
        
        # Add both to the same cell to stack them
        grid.addWidget(card, 0, 0)
        grid.addWidget(btn, 0, 0)
        
        parent_layout.addWidget(container)
        return btn, card