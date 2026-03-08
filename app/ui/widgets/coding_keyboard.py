from PyQt6.QtWidgets import QWidget, QSizePolicy
from core.input.input_events import Action
from app.ui.widgets.key_button import KeyButton
from PyQt6.QtCore import QTimer


# ================= MAIN GRID =================

MAIN_GRID = [
    ("NUM", ["0","1","2","3","4"]),
    ("ABC", ["a","b","c"]),
    ("DEF", ["d","e","f"]),
    ("GHI", ["g","h","i"]),
   
]


# ================= SYMBOLS =================

SYMBOL_KEYS = [
    "+","-","*","/",
    "=","==","!=","%",
    "<",">","(",")",
]


# ================= PYTHON SHORTCUTS =================

CODE_SNIPPETS = [
    "print()",
    "for i in range():\n\t",
    "if :\n\t",
    "while True:\n\t",
    "def function():\n\t",
    "import ",
    "class MyClass:\n\tdef __init__(self):\n\t\t",
    "return "
]


# ================= GROUP BUTTON =================

class ExpandGroup(KeyButton):

    def __init__(self, label, keys, keyboard):
        super().__init__(label, Action.NONE, None, keyboard)
        self.keys = keys
        self.keyboard = keyboard

    def select(self):
        self.keyboard.show_group(self.keys)
        return Action.NONE


# ================= TYPING KEYBOARD =================

class CodingKeyboard(QWidget):

    def __init__(self, parent=None, main_window=None):

        super().__init__(parent)

        self.main_window = main_window
        self.focusables = []

        self.setStyleSheet(
            "background-color: rgba(20,20,20,240);"
        )

        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )

        self.setMinimumSize(300, 300)

       

        self.build_main()
        self.hide()


# ================= CLEAR KEYS =================

    def clear_keys(self):

        for w in self.findChildren(KeyButton):
            w.setParent(None)

        self.focusables.clear()


# ================= MAIN KEYBOARD =================

    def build_main(self):

        self.clear_keys()

        spacing_x = 200
        spacing_y = 150

        cols = 3
        rows = 4

        board_width = cols * spacing_x
        board_height = rows * spacing_y

        screen_w = self.width()
        screen_h = self.height()

        x_start = (screen_w - board_width) // 2
        y_start = (screen_h - board_height) // 2 + 40

        for i, (label, keys) in enumerate(MAIN_GRID):

            btn = ExpandGroup(label, keys, self)

            row = i // cols
            col = i % cols

            btn.move(
                x_start + col * spacing_x,
                y_start + row * spacing_y
            )

            btn.setMinimumSize(320, 160)
            btn.show()

            self.focusables.append(btn)

        bottom_y = y_start + (rows - 1) * spacing_y + 90

        sym = KeyButton("SYM", Action.NONE, None, self)
        sym.move(x_start, bottom_y)
        sym.setMinimumSize(140,70)
        sym.show()
        sym.select = self.show_symbols

        code = KeyButton("CODE", Action.NONE, None, self)
        code.move(x_start + spacing_x, bottom_y)
        code.setMinimumSize(140,70)
        code.show()
        code.select = self.show_code

        ctrl = KeyButton("CTRL", Action.NONE, None, self)
        ctrl.move(x_start + spacing_x*2, bottom_y)
        ctrl.setMinimumSize(140,70)
        ctrl.show()
        ctrl.select = self.show_controls

        self.focusables += [sym, code, ctrl]

        if self.main_window:
            self.main_window.focusables = self.focusables

    


# ================= LETTER GROUP =================

    def show_group(self, keys):

        self.clear_keys()

        x = 300
        y = 200
        spacing = 120

        for i, k in enumerate(keys):

            btn = KeyButton(k, Action.INSERT_CHAR, k, self)

            btn.move(
                x + (i % 5) * spacing,
                y + (i // 5) * spacing
            )

            btn.show()
            self.focusables.append(btn)

            if k.isalpha():

                cap = KeyButton(k.upper(), Action.INSERT_CHAR, k.upper(), self)

                cap.move(
                    x + (i % 5) * spacing,
                    y + 200 + (i // 5) * spacing
                )

                cap.show()
                self.focusables.append(cap)

        self.add_back_button()

        if self.main_window:
            self.main_window.focusables = self.focusables

        


# ================= SYMBOLS =================

    def show_symbols(self):

        self.clear_keys()

        x = 200
        y = 200
        spacing = 120

        for i, sym in enumerate(SYMBOL_KEYS):

            btn = KeyButton(sym, Action.INSERT_CHAR, sym, self)

            btn.move(
                x + (i % 6) * spacing,
                y + (i // 6) * spacing
            )

            btn.show()
            self.focusables.append(btn)

        self.add_back_button()

        if self.main_window:
            self.main_window.focusables = self.focusables

        


# ================= CODE SNIPPETS =================

    def show_code(self):

        self.clear_keys()

        x = 60
        y = 60
        spacing = 100

        for i, code in enumerate(CODE_SNIPPETS):

            btn = KeyButton(code, Action.INSERT_CHAR, code, self)

            btn.move(x, y + i*spacing)

            btn.setMinimumSize(400,80)
            btn.show()

            self.focusables.append(btn)

        self.add_back_button()

        if self.main_window:
            self.main_window.focusables = self.focusables

      


# ================= CONTROLS =================

    def show_controls(self):

        self.clear_keys()

        x = 400
        y = 250
        spacing = 120

        space = KeyButton("SPACE", Action.SPACE, None, self)
        space.move(x, y)
        space.show()

        tab = KeyButton("TAB", Action.INSERT_CHAR, "    ", self)
        tab.move(x, y + spacing)
        tab.show()

        enter = KeyButton("ENTER", Action.INSERT_CHAR, "\n", self)
        enter.move(x, y + 2*spacing)
        enter.show()

        back = KeyButton("⌫", Action.BACKSPACE, None, self)
        back.move(x + 200, y)
        back.show()

        done = KeyButton("DONE", Action.DONE, None, self)
        done.move(x + 200, y + spacing)
        done.show()

        self.focusables += [space, tab, enter, back, done]

        self.add_back_button()

        if self.main_window:
            self.main_window.focusables = self.focusables

     


# ================= BACK BUTTON =================

    def add_back_button(self):

        back = KeyButton("BACK", Action.NONE, None, self)

        back.move(80, 80)
        back.show()

        back.select = self.back_to_main

        self.focusables.append(back)


# ================= RETURN MAIN =================

    def back_to_main(self):

        self.build_main()

        if self.main_window:
            self.main_window.focusables = self.focusables

   

        return Action.NONE


# ================= KEY HANDLER =================

    def handle_key(self, action, value):

        if action in (
            Action.INSERT_CHAR,
            Action.SPACE,
            Action.BACKSPACE,
            Action.DONE
        ):
            return action, value

        return None, None


# ================= RESIZE =================

    def resizeEvent(self, event):

        super().resizeEvent(event)

        if self.isVisible():
            self.build_main()




   


    