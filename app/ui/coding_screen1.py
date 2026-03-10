'''from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTextEdit
from app.ui.widgets.gaze_button import GazeButton
from app.ui.widgets.focusable import FocusableWidget
from core.input.input_events import Action
import io
import contextlib
from PyQt6.QtGui import QTextCursor
from PyQt6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from PyQt6.QtCore import QRegularExpression
from PyQt6.QtWidgets import QStackedLayout


class CodeEditor(QTextEdit):

    pairs = {
        "(": ")",
        "[": "]",
        "{": "}",
        '"': '"',
        "'": "'"
    }

    def keyPressEvent(self, event):

        key_text = event.text()

        if key_text in self.pairs:

            cursor = self.textCursor()
            cursor.insertText(key_text + self.pairs[key_text])
            cursor.movePosition(QTextCursor.MoveOperation.Left)
            self.setTextCursor(cursor)
            return

        if event.key() == 16777220:

            cursor = self.textCursor()
            line = cursor.block().text()

            indent = len(line) - len(line.lstrip(" "))

            super().keyPressEvent(event)

            cursor = self.textCursor()
            cursor.insertText(" " * indent)

            if line.strip().endswith(":"):
                cursor.insertText("    ")

            return

        super().keyPressEvent(event)


class PythonHighlighter(QSyntaxHighlighter):

    def __init__(self, document):
        super().__init__(document)

        self.rules = []

        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#569CD6"))
        keyword_format.setFontWeight(QFont.Weight.Bold)

        keywords = [
            "and","as","assert","break","class","continue","def","del",
            "elif","else","except","False","finally","for","from",
            "global","if","import","in","is","lambda","None",
            "nonlocal","not","or","pass","raise","return",
            "True","try","while","with","yield"
        ]

        for word in keywords:
            pattern = QRegularExpression(rf"\b{word}\b")
            self.rules.append((pattern, keyword_format))

        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#CE9178"))

        self.rules.append((QRegularExpression(r'"[^"]*"'), string_format))
        self.rules.append((QRegularExpression(r"'[^']*'"), string_format))

        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#6A9955"))

        self.rules.append((QRegularExpression(r"#.*"), comment_format))

    def highlightBlock(self, text):

        for pattern, fmt in self.rules:

            matches = pattern.globalMatch(text)

            while matches.hasNext():

                match = matches.next()

                start = match.capturedStart()
                length = match.capturedLength()

                self.setFormat(start, length, fmt)


class CodingScreen(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        main_layout = QVBoxLayout()

        io_layout = QHBoxLayout()

        self.editor = CodeEditor()
        self.editor.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        self.highlighter = PythonHighlighter(self.editor.document())

        self.output = QTextEdit()
        self.output.setReadOnly(True)

        self.output.setStyleSheet("""
        QTextEdit {
            background-color: black;
            color: #00FF66;
            font-family: Consolas;
            font-size: 18px;
        }
        """)

        io_layout.addWidget(self.editor)
        io_layout.addWidget(self.output)

        main_layout.addLayout(io_layout)

        self.panel_container = QWidget()
        self.panel_layout = QStackedLayout()
        self.panel_container.setLayout(self.panel_layout)

        main_layout.addWidget(self.panel_container)

        self.fixed_controls = QWidget()
        fixed_layout = QHBoxLayout()

        self.btn_backspace = GazeButton("Backspace", Action.BACKSPACE,None,self)
        self.btn_space = GazeButton("Space", Action.INSERT_CODE_CHAR, " ", self)
        self.btn_enter = GazeButton("Enter", Action.INSERT_CODE_CHAR, "\n", self)

        fixed_layout.addWidget(self.btn_backspace)
        fixed_layout.addWidget(self.btn_space)
        fixed_layout.addWidget(self.btn_enter)

        self.fixed_controls.setLayout(fixed_layout)
        main_layout.addWidget(self.fixed_controls)

        self.setLayout(main_layout)

        # ---------------- MAIN PANEL ----------------

        self.main_panel = QWidget()
        main_buttons = QVBoxLayout()

        self.btn_templates = GazeButton("Templates", Action.OPEN_TEMPLATES, None, self)
        self.btn_keyboard  = GazeButton("Keyboard", Action.OPEN_CKEYBOARD, None, self)
        self.btn_run       = GazeButton("Run Code", Action.RUN_CODE, None, self)
        self.btn_clear     = GazeButton("Clear", Action.CLEAR_EDITOR, None, self)

        main_buttons.addWidget(self.btn_run)
        main_buttons.addWidget(self.btn_templates)
        main_buttons.addWidget(self.btn_keyboard)
        main_buttons.addWidget(self.btn_clear)

        self.main_panel.setLayout(main_buttons)
        self.panel_layout.addWidget(self.main_panel)

        # ---------------- TEMPLATE PANEL ----------------

        self.template_panel = QWidget()
        tpl_layout = QVBoxLayout()

        self.btn_if = GazeButton("if", Action.INSERT_TEMPLATE, "if condition:\n    ", self)
        self.btn_for = GazeButton("for", Action.INSERT_TEMPLATE, "for i in range():\n    ",self)
        self.btn_while = GazeButton("while", Action.INSERT_TEMPLATE, "while condition:\n    ", self)
        self.btn_def = GazeButton("def", Action.INSERT_TEMPLATE, "def function():\n    ", self)
        self.btn_print = GazeButton("print()", Action.INSERT_TEMPLATE, "print()", self)

        self.btn_template_back = GazeButton("Back", Action.OPEN_MAIN, None,self)

        tpl_layout.addWidget(self.btn_if)
        tpl_layout.addWidget(self.btn_for)
        tpl_layout.addWidget(self.btn_while)
        tpl_layout.addWidget(self.btn_def)
        tpl_layout.addWidget(self.btn_print)
        tpl_layout.addWidget(self.btn_template_back)

        self.template_panel.setLayout(tpl_layout)
        self.panel_layout.addWidget(self.template_panel)

        # ---------------- KEYBOARD PANEL ----------------

        self.keyboard_panel = QWidget()
        kb_layout = QVBoxLayout()

        self.btn_alpha = GazeButton("Alpha", Action.OPEN_ALPHA, None,self)
        self.btn_num = GazeButton("Num", Action.OPEN_NUM, None,self)
        self.btn_sym = GazeButton("Sym", Action.OPEN_SYM, None,self)

        self.btn_keyboard_back = GazeButton("Back", Action.OPEN_MAIN, None,self)

        kb_layout.addWidget(self.btn_alpha)
        kb_layout.addWidget(self.btn_num)
        kb_layout.addWidget(self.btn_sym)
        kb_layout.addWidget(self.btn_keyboard_back)

        self.keyboard_panel.setLayout(kb_layout)
        self.panel_layout.addWidget(self.keyboard_panel)

        # ---------------- ALPHA PANEL ----------------

        self.alpha_panel = QWidget()

        alpha_rows = [
            ["ABC", "DEF", "GHI"],
            ["JKL", "MNO", "PQR"],
            ["STU", "VWX", "YZ"]
        ]

        alpha_layout = self.build_grid(alpha_rows, letters=True)

        self.btn_alpha_back = GazeButton("Back", Action.OPEN_CKEYBOARD, None,self)
        alpha_layout.addWidget(self.btn_alpha_back)

        self.alpha_panel.setLayout(alpha_layout)
        self.panel_layout.addWidget(self.alpha_panel)

        # ---------------- NUM PANEL ----------------

        self.num_panel = QWidget()

        num_rows = [
            ["1","2","3"],
            ["4","5","6"],
            ["7","8","9"],
            ["0"]
        ]

        num_layout = self.build_grid(num_rows)

        self.btn_num_back = GazeButton("Back", Action.OPEN_CKEYBOARD, None,self)
        num_layout.addWidget(self.btn_num_back)

        self.num_panel.setLayout(num_layout)
        self.panel_layout.addWidget(self.num_panel)

        # ---------------- SYMBOL PANEL ----------------

        self.sym_panel = QWidget()

        sym_rows = [
            ["(", ":"],
            ["+", "-", "*"],
            ["/", "=", ","]
        ]

        sym_layout = self.build_grid(sym_rows)

        self.btn_sym_back = GazeButton("Back", Action.OPEN_CKEYBOARD,None,self)
        sym_layout.addWidget(self.btn_sym_back)

        self.sym_panel.setLayout(sym_layout)
        self.panel_layout.addWidget(self.sym_panel)

        self.panel_layout.setCurrentWidget(self.main_panel)

    def backspace(self):

        cursor = self.editor.textCursor()
        cursor.deletePreviousChar()
        self.editor.setTextCursor(cursor)

    def build_grid(self, rows, letters=False):

        layout = QVBoxLayout()
        layout.setSpacing(25)
        layout.setContentsMargins(30,20,30,20)

        for row in rows:

            h = QHBoxLayout()

            for key in row:

                if letters:
                    btn = GazeButton(key, Action.OPEN_LETTER_GROUP, key, self)
                else:
                    btn = GazeButton(key, Action.INSERT_CODE_CHAR, key, self)

                btn.setFixedHeight(90)
                btn.setMinimumWidth(160)

                h.addWidget(btn)

            layout.addLayout(h)

        return layout

    def insert_template(self, text):

        cursor = self.editor.textCursor()
        cursor.insertText(text)
        self.editor.setTextCursor(cursor)

    def insert_text(self, text):

        cursor = self.editor.textCursor()
        cursor.insertText(text)
        self.editor.setTextCursor(cursor)

    def clear_editor(self):
        self.editor.clear()

    def run_code(self):

        code = self.editor.toPlainText()
        buffer = io.StringIO()

        try:

            with contextlib.redirect_stdout(buffer):
                exec(code, {})

            output = buffer.getvalue()

            if output.strip() == "":
                output = "Code executed successfully."

            self.output.setPlainText(output)

        except Exception as e:

            self.output.setPlainText(str(e))

    def get_focusables(self):

        focusables = []

        for child in self.findChildren(FocusableWidget):

            if child.isVisible():
                focusables.append(child)

        return focusables
'''