from PyQt6.QtWidgets import QWidget
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

        self.mode = "GROUP"          # GROUP | LETTER | NUMBER
        self.selected_group = None
        self.focusables = []

        self.hide()
        self.build_group_mode()
    def clear_keys(self):
        for w in self.findChildren(KeyButton):
            w.setParent(None)
        self.focusables.clear()
    def build_group_mode(self):
        self.clear_keys()
        self.mode = "GROUP"

        x, y = 100, 80
        col = 0

        for group in GROUPS.keys():
            btn = KeyButton(group, Action.GROUP_SELECT, group, self)
            btn.move(x + col * 200, y)
            btn.show()

            self.focusables.append(btn)
            col += 1

            if col == 4:
                col = 0
                y += 120

        # bottom row
        bottom_y = y + 140

        space = KeyButton("SPACE", Action.SPACE, None, self)
        space.move(100, bottom_y)
        space.show()

        num = KeyButton("123", Action.NUMBER_MODE, None, self)
        num.move(320, bottom_y)
        num.show()

        back = KeyButton("⌫", Action.BACKSPACE, None, self)
        back.move(540, bottom_y)
        back.show()

        done = KeyButton("DONE", Action.DONE, None, self)
        done.move(760, bottom_y)
        done.show()

        self.focusables += [space, num, back, done]
    def build_letter_mode(self, group):
            self.clear_keys()
            self.mode = "LETTER"
            self.selected_group = group

            letters = GROUPS[group]

            x, y = 200, 150
            for i, ch in enumerate(letters):
                btn = KeyButton(ch, Action.INSERT_CHAR, ch, self)
                btn.move(x + i * 200, y)
                btn.show()
                self.focusables.append(btn)

            y += 140

            space = KeyButton("SPACE", Action.SPACE, None, self)
            space.move(200, y)
            space.show()

            back = KeyButton("⌫", Action.BACKSPACE, None, self)
            back.move(420, y)
            back.show()

            back_btn = KeyButton("BACK", Action.BACK_MODE, None, self)
            back_btn.move(640, y)
            back_btn.show()

            self.focusables += [space, back, back_btn]
    def build_number_mode(self):
        self.clear_keys()
        self.mode = "NUMBER"

        nums = ["1","2","3","4","5","6","7","8","9"]
        x, y = 200, 120
        i = 0

        for n in nums:
            btn = KeyButton(n, Action.INSERT_CHAR, n, self)
            btn.move(x + (i % 3) * 200, y + (i // 3) * 120)
            btn.show()
            self.focusables.append(btn)
            i += 1

        zero = KeyButton("0", Action.INSERT_CHAR, "0", self)
        zero.move(200, y + 3 * 120)
        zero.show()

        back = KeyButton("⌫", Action.BACKSPACE, None, self)
        back.move(420, y + 3 * 120)
        back.show()

        back_btn = KeyButton("BACK", Action.BACK_MODE, None, self)
        back_btn.move(640, y + 3 * 120)
        back_btn.show()

        self.focusables += [zero, back, back_btn]
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
            Action.DONE
        ):
            return action, value

        return None, None
