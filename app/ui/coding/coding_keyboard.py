from PyQt6.QtWidgets import QWidget, QGridLayout
from core.input.input_events import Action
from app.ui.coding.coding_keybutton import CodingKeyButton


ALPHA_GROUPS = [
    ("ABC", ["a","b","c"]),
    ("DEF", ["d","e","f"]),
    ("GHI", ["g","h","i"]),
    ("JKL", ["j","k","l"]),
    ("MNO", ["m","n","o"]),
    ("PQR", ["p","q","r"]),
    ("STU", ["s","t","u"]),
    ("VWX", ["v","w","x"]),
    ("YZ", ["y","z"]),
]

NUM_KEYS = [
    "1","2","3",
    "4","5","6",
    "7","8","9",
    "0"
]

SYM_KEYS = [
    "+","-","*","/",
    "=","!=","%","(","<",">",":",","
]


class CodingKeyboard(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.focusables = []

        self.show_main()

    # ---------------- CLEAR ----------------

    def clear(self):

        while self.layout.count():
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        self.focusables = []

    # ---------------- MAIN ----------------

    def show_main(self):

        self.clear()

        alpha = CodingKeyButton("Alpha", Action.OPEN_ALPHA, None, self)
        num = CodingKeyButton("Num", Action.OPEN_NUM, None, self)
        sym = CodingKeyButton("Sym", Action.OPEN_SYM, None, self)
        back = CodingKeyButton("Back", Action.OPEN_MAIN, None, self)

        self.layout.addWidget(alpha,0,0)
        self.layout.addWidget(num,0,1)
        self.layout.addWidget(sym,0,2)
        self.layout.addWidget(back,1,1)

        self.focusables = [alpha,num,sym,back]

    # ---------------- ALPHA ----------------

    def show_alpha(self):

        self.clear()

        row = 0
        col = 0

        for label, keys in ALPHA_GROUPS:

            btn = CodingKeyButton(label, Action.OPEN_GROUP, keys, self)

            self.layout.addWidget(btn,row,col)
            self.focusables.append(btn)

            col += 1

            if col == 3:
                col = 0
                row += 1

        back = CodingKeyButton("Back", Action.OPEN_CKEYBOARD, None, self)

        self.layout.addWidget(back,row+1,1)
        self.focusables.append(back)

    # ---------------- GROUP ----------------

    def show_group(self, keys):

        self.clear()

        row = 0
        col = 0

        for letter in keys:

            btn = CodingKeyButton(letter, Action.INSERT_CHAR, letter, self)

            self.layout.addWidget(btn,row,col)
            self.focusables.append(btn)

            col += 1

        back = CodingKeyButton("Back", Action.OPEN_ALPHA, None, self)

        self.layout.addWidget(back,row+1,1)
        self.focusables.append(back)

    # ---------------- NUM ----------------

    def show_num(self):

        self.clear()

        row = 0
        col = 0

        for key in NUM_KEYS:

            btn = CodingKeyButton(key, Action.INSERT_CHAR, key, self)

            self.layout.addWidget(btn,row,col)
            self.focusables.append(btn)

            col += 1

            if col == 3:
                col = 0
                row += 1

        back = CodingKeyButton("Back", Action.OPEN_CKEYBOARD, None, self)

        self.layout.addWidget(back,row+1,1)
        self.focusables.append(back)

    # ---------------- SYMBOLS ----------------

    def show_sym(self):

        self.clear()

        row = 0
        col = 0

        for key in SYM_KEYS:

            btn = CodingKeyButton(key, Action.INSERT_CHAR, key, self)

            self.layout.addWidget(btn,row,col)
            self.focusables.append(btn)

            col += 1

            if col == 4:
                col = 0
                row += 1

        back = CodingKeyButton("Back", Action.OPEN_CKEYBOARD, None, self)

        self.layout.addWidget(back,row+1,1)
        self.focusables.append(back)