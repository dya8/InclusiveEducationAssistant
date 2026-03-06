from PyQt6.QtWidgets import QWidget, QGridLayout, QSizePolicy
from core.input.input_events import Action
from app.ui.widgets.key_button import KeyButton

GROUPS = {
    "ABC": ["A", "B", "C"],
    "DEF": ["D", "E", "F"],
    "GHI": ["G", "H", "I"],
    "JKL": ["J", "K", "L"],
    "MNO": ["M", "N", "O"],
    "PQRS": ["P", "Q", "R", "S"],
    "TUV": ["T", "U", "V"],
    "WXYZ": ["W", "X", "Y", "Z"]
}

class TypingKeyboard(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.mode = "GROUP"
        self.selected_group = None
        self.focusables = []

        self.grid = QGridLayout()
        self.grid.setContentsMargins(80, 30, 80, 30)
        self.grid.setHorizontalSpacing(40)
        self.grid.setVerticalSpacing(30)

        self.setLayout(self.grid)

        self.build_group_mode()

    def clear_keys(self):
        while self.grid.count():
            child = self.grid.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        self.focusables.clear()

    # ==================================================
    # GROUP MODE
    # ==================================================
    def build_group_mode(self):
        self.clear_keys()
        save = KeyButton("SAVE", Action.SAVE_NOTE, None, self)
        save.setMinimumSize(220, 320)
        save.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        save.setMinimumSize(220, 320)
        save.setStyleSheet("""
        background:#2ecc71;
        font-size:30px;
        font-weight:bold;
        """)

        self.mode = "GROUP"

        row = 0
        col = 0

        for group in GROUPS.keys():
            btn = KeyButton(group, Action.GROUP_SELECT, group, self)
            btn.setMinimumSize(220, 150)
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

            self.grid.addWidget(btn, row, col)
            self.focusables.append(btn)

            col += 1
            if col == 4:
                col = 0
                row += 1
        # SAVE BUTTON (right side vertical)
        self.grid.addWidget(save, 0, 4, 3, 1)
        self.focusables.append(save)
        # bottom row
        row += 1

        space = KeyButton("SPACE", Action.SPACE, None, self)
        num = KeyButton("123", Action.NUMBER_MODE, None, self)
        clear = KeyButton("CLEAR", Action.BACKSPACE, None, self)
        done = KeyButton("DONE", Action.DONE, None, self)

        for btn in [space, num, clear, done]:
            btn.setMinimumSize(220, 150)
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.grid.addWidget(space, row, 0)
        self.grid.addWidget(num, row, 1)
        self.grid.addWidget(clear, row, 2)
        self.grid.addWidget(done, row, 3)

        self.focusables += [space, num, clear, done]

        self._apply_row_stretch(row)

    # ==================================================
    # LETTER MODE
    # ==================================================
    def build_letter_mode(self, group):
        self.clear_keys()
        self.mode = "LETTER"
        self.selected_group = group

        letters = GROUPS[group]

        for col, ch in enumerate(letters):
            btn = KeyButton(ch, Action.INSERT_CHAR, ch, self)
            btn.setMinimumSize(220, 150)
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

            self.grid.addWidget(btn, 0, col)
            self.focusables.append(btn)

        # bottom row
        space = KeyButton("SPACE", Action.SPACE, None, self)
        back = KeyButton("⌫", Action.BACKSPACE, None, self)
        back_btn = KeyButton("BACK", Action.BACK_MODE, None, self)

        for col, btn in enumerate([space, back, back_btn]):
            btn.setMinimumSize(220, 150)
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

            self.grid.addWidget(btn, 1, col)
            self.focusables.append(btn)

        self._apply_row_stretch(1)

    # ==================================================
    # NUMBER MODE
    # ==================================================
    def build_number_mode(self):
        self.clear_keys()
        self.mode = "NUMBER"

        nums = ["1","2","3","4","5","6","7","8","9"]

        for i, n in enumerate(nums):
            row = i // 3
            col = i % 3

            btn = KeyButton(n, Action.INSERT_CHAR, n, self)
            btn.setMinimumSize(170, 95)
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

            self.grid.addWidget(btn, row, col)
            self.focusables.append(btn)

        zero = KeyButton("0", Action.INSERT_CHAR, "0", self)
        back = KeyButton("⌫", Action.BACKSPACE, None, self)
        back_btn = KeyButton("BACK", Action.BACK_MODE, None, self)

        for col, btn in enumerate([zero, back, back_btn]):
            btn.setMinimumSize(170, 95)
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

            self.grid.addWidget(btn, 3, col)
            self.focusables.append(btn)

        self._apply_row_stretch(3)

    # ==================================================
    # ROW STRETCH BALANCE
    # ==================================================
    def _apply_row_stretch(self, last_row):
        for r in range(last_row + 1):
            self.grid.setRowStretch(r, 1)
        for c in range(5):
            self.grid.setColumnStretch(c, 1)

    # ==================================================
    # ACTION HANDLER
    # ==================================================
    def handle_key(self, action, value):
        if action == Action.GROUP_SELECT:
            self.build_letter_mode(value)

        elif action == Action.NUMBER_MODE:
            self.build_number_mode()

        elif action == Action.BACK_MODE:
            self.build_group_mode()

        elif action in (
            Action.INSERT_CHAR,
            Action.SPACE,
            Action.BACKSPACE,
            Action.DONE,
            Action.SAVE_NOTE,
            Action.CLEAR_TEXT
        ):
            return action, value

        return None, None