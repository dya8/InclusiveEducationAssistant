'''import subprocess
import tempfile

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
        QPlainTextEdit,

    QLabel
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from app.ui.widgets.test_button import TestButton
from core.input.input_events import Action
from app.state.app_state import AppState
from app.ui.widgets.coding_keyboard import CodingKeyboard
from app.ui.widgets.code_editor import CodeEditor
from PyQt6.QtGui import QTextOption





class CodingScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window

        # ================= MAIN LAYOUT =================
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # ================= TITLE =================
        title = QLabel("Assistive Coding - Python")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        main_layout.addWidget(title)

        # ================= CODE EDITOR =================
        self.editor =QPlainTextEdit()
        self.editor.setPlaceholderText("Write your Python code here...")
        self.editor.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.editor.setFont(QFont("Consolas", 14))
        self.editor.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        main_layout.addWidget(self.editor)
        self.editor.setFixedHeight(300)
        self.editor.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.editor.setWordWrapMode(QTextOption.WrapMode.NoWrap)
        # ================= TYPING KEYBOARD =================
      
        
        self.keyboard = CodingKeyboard(self, self.main_window)
        #main_layout.addWidget(self.keyboard)
        self.keyboard.hide()
        self.typing_active = False

        # ================= SNIPPET BUTTONS =================
        snippet_layout = QHBoxLayout()

        self.btn_print = self._create_button("print()", snippet_layout)
        self.btn_if = self._create_button("if", snippet_layout)
        self.btn_for = self._create_button("for", snippet_layout)
        self.btn_def = self._create_button("def", snippet_layout)
        self.btn_while = self._create_button("while", snippet_layout)

        main_layout.addLayout(snippet_layout)
        snippet_layout.setSpacing(15)

        # ================= OUTPUT =================
        output_label = QLabel("Output:")
        output_label.setStyleSheet("font-weight: bold;")
        main_layout.addWidget(output_label)

        self.output_console = QPlainTextEdit()
        self.output_console.setReadOnly(True)
        self.output_console.setFont(QFont("Consolas", 12))
        self.output_console.setStyleSheet(
            "background-color: #1e1e1e; color: #00ff00;"
        )
        main_layout.addWidget(self.output_console)
        self.output_console.setFixedHeight(200)

        # ================= CONTROL BUTTONS =================
        control_layout = QHBoxLayout()
        
        
        self.btn_run = self._create_button("RUN CODE", control_layout)
        self.btn_keyboard = self._create_button("OPEN KEYBOARD", control_layout)
        self.btn_clear = self._create_button("CLEAR OUTPUT", control_layout)
        self.btn_back = self._create_button("BACK", control_layout)
        
        self.btn_keyboard.action = Action.OPEN_TYPING_KEYBOARD

        main_layout.addLayout(control_layout)
        # ================= KEYBOARD BUTTON =================
      

        # ================= ACTION ASSIGNMENT =================
        self.btn_run.action = Action.RUN_CODE
        self.btn_clear.action = Action.CLEAR_OUTPUT
        self.btn_back.action = Action.BACK

        # Snippet buttons return INSERT_SNIPPET
        self.btn_print.action = Action.INSERT_SNIPPET
        self.btn_if.action = Action.INSERT_SNIPPET
        self.btn_for.action = Action.INSERT_SNIPPET
        self.btn_def.action = Action.INSERT_SNIPPET
        self.btn_while.action = Action.INSERT_SNIPPET

        # Map snippets
        self.snippet_map = {
            self.btn_print: "print()",
            self.btn_if: "if \n\t",
            self.btn_for: "for i in range():\n\t", 
            self.btn_def: "def function():\n\t",
            self.btn_while: "while True:\n\t"   
        }

        # Focusable list for MainWindow
        self.focusables = [
    self.btn_print,
    self.btn_if,
    self.btn_for,
    self.btn_def,
    self.btn_while,
    self.btn_run,
    self.btn_clear,
    self.btn_keyboard,   # 👈 add this
    self.btn_back
]
    # =====================================================
    # BUTTON FACTORY
    # =====================================================

    def _create_button(self, text, layout):
        btn = TestButton(text, self)
        btn.setMinimumSize(220, 70)  
        layout.addWidget(btn)
        return btn

    # =====================================================
    # INSERT TEXT
    # =====================================================

    def insert_text(self, text):
        cursor = self.editor.textCursor()
        cursor.insertText(text)
        self.editor.setTextCursor(cursor)
        self.editor.setFocus()
    def open_keyboard(self):
        self.keyboard.show()
        self.typing_active = True
    
    

    # =====================================================
    # RUN CODE
    # =====================================================

    def run_code(self):
        code = self.editor.toPlainText()

        if not code.strip():
            self.output_console.setPlainText("No code to execute.")
            return

        try:
            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".py",
                mode="w",
                encoding="utf-8"
            ) as temp_file:
                temp_file.write(code)
                temp_path = temp_file.name

            result = subprocess.run(
                ["python", temp_path],
                capture_output=True,
                text=True,
                timeout=3
            )

            output = result.stdout + result.stderr
            if not output:
                output = "Program executed successfully (no output)."

            self.output_console.setPlainText(output)

        except subprocess.TimeoutExpired:
            self.output_console.setPlainText(
                "Execution timed out (possible infinite loop)."
            )

        except Exception as e:
            self.output_console.setPlainText(f"Error:\n{str(e)}")

    #====================================================
    # BUILD KEYBOARDS
    #====================================================
    def handle_keyboard_action(self, action, value):
        if action == Action.INSERT_CHAR:
            self.insert_text(value)

        elif action == Action.SPACE:
            self.insert_text(" ")

        elif action == Action.BACKSPACE:
            cursor = self.editor.textCursor()
            cursor.deletePreviousChar()
            self.editor.setTextCursor(cursor)
            self.editor.setFocus()

        elif action == Action.DONE:
            
            self.keyboard.scan_timer.stop()
            self.keyboard.hide()
            self.typing_active = False
            self.main_window.restore_normal_input()
  
    
    # =====================================================
    # CLEAR OUTPUT
    # =====================================================

    def clear_output(self):
        self.output_console.clear()

    # =====================================================
    # HANDLE SNIPPET FROM MAINWINDOW
    # =====================================================

    def handle_snippet(self, button):
        if button in self.snippet_map:
            self.insert_text(self.snippet_map[button])

    # =====================================================
    # BACK
    # =====================================================

    def go_back(self):
        self.main_window.switch_state(AppState.HOME)
        '''
import subprocess
import tempfile

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QPlainTextEdit
)

from PyQt6.QtGui import QFont, QTextOption
from PyQt6.QtCore import Qt

from app.ui.widgets.test_button import TestButton
from core.input.input_events import Action
from app.state.app_state import AppState


class CodingScreen(QWidget):

    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window

        # ================= MAIN LAYOUT =================
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # ================= TITLE =================
        title = QLabel("Assistive Coding - Python")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size:20px;font-weight:bold;")
        main_layout.addWidget(title)

        # ================= TOP AREA =================
        top_layout = QHBoxLayout()
        main_layout.addLayout(top_layout)

        # ===== CODE EDITOR =====
        self.editor = QPlainTextEdit()
        self.editor.setPlaceholderText("Write Python code here...")
        self.editor.setFont(QFont("Consolas", 14))
        self.editor.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.editor.setWordWrapMode(QTextOption.WrapMode.NoWrap)
        self.editor.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOn
        )

        top_layout.addWidget(self.editor, 2)

        # ===== OUTPUT CONSOLE =====
        self.output_console = QPlainTextEdit()
        self.output_console.setReadOnly(True)
        self.output_console.setFont(QFont("Consolas", 12))
        self.output_console.setStyleSheet(
            "background-color:#1e1e1e;color:#00ff00;"
        )

        top_layout.addWidget(self.output_console, 1)

        # ================= BOTTOM AREA =================
        bottom_layout = QHBoxLayout()
        main_layout.addLayout(bottom_layout)

        # ===== SNIPPET BUTTONS =====
        snippet_layout = QVBoxLayout()
        bottom_layout.addLayout(snippet_layout, 1)

        self.btn_print = self._create_button("print()", snippet_layout)
        self.btn_if = self._create_button("if", snippet_layout)
        self.btn_for = self._create_button("for", snippet_layout)
        self.btn_def = self._create_button("def", snippet_layout)
        self.btn_while = self._create_button("while", snippet_layout)

        # snippet actions
        self.btn_print.action = Action.INSERT_SNIPPET
        self.btn_if.action = Action.INSERT_SNIPPET
        self.btn_for.action = Action.INSERT_SNIPPET
        self.btn_def.action = Action.INSERT_SNIPPET
        self.btn_while.action = Action.INSERT_SNIPPET

        # snippet map
        self.snippet_map = {
            self.btn_print: "print(",
            self.btn_if: "if:",
            self.btn_for: "for i in range(",
            self.btn_def: "def function(",
            self.btn_while: "while True:\n\t"
        }

        # ===== KEYBOARD =====
        keyboard_layout = QGridLayout()
        bottom_layout.addLayout(keyboard_layout, 2)

        self.keyboard_buttons = []

        # ===== SPECIAL KEYS (TOP ROW) =====
       
        
        backspace_btn = TestButton("⌫", self)
        backspace_btn.setMinimumSize(120,70)
        backspace_btn.action = Action.BACKSPACE
        backspace_btn.value = None

        space_btn = TestButton("SPACE", self)
        space_btn.setMinimumSize(120,70)
        space_btn.action = Action.INSERT_CHAR
        space_btn.value = " "

        enter_btn = TestButton("ENTER", self)
        enter_btn.setMinimumSize(120,70)
        enter_btn.action = Action.INSERT_CHAR
        enter_btn.value = "\n"

        

        keyboard_layout.addWidget(backspace_btn, 0, 0)
        keyboard_layout.addWidget(enter_btn, 0, 1)
        keyboard_layout.addWidget(space_btn, 0, 2)

        self.keyboard_buttons.extend([backspace_btn,enter_btn,space_btn])


        # ===== NUMBER + SYMBOL KEYS =====
        keys = [
            ["1","2","3"],
            ["n","i","j"],
            [":","+","-"],
            ["*","/","="]
        ]

        for r, row in enumerate(keys):
            for c, key in enumerate(row):

                btn = TestButton(key, self)
                btn.setMinimumSize(90,70)

                btn.action = Action.INSERT_CHAR
                btn.value = key

                keyboard_layout.addWidget(btn, r+1, c)   # r+1 because row 0 is special keys

                self.keyboard_buttons.append(btn)



        # ===== CONTROL BUTTONS =====
        control_layout = QHBoxLayout()
        main_layout.addLayout(control_layout)

        self.btn_run = TestButton("RUN CODE", self)
        self.btn_clear_output = TestButton("CLEAR OUTPUT", self)
        self.btn_back = TestButton("BACK", self)

        self.btn_run.action = Action.RUN_CODE
        self.btn_clear_output.action = Action.CLEAR_OUTPUT
        self.btn_back.action = Action.BACK

        control_layout.addWidget(self.btn_run)
        control_layout.addWidget(self.btn_clear_output)
        control_layout.addWidget(self.btn_back)

        # ===== FOCUSABLE ELEMENTS =====
        self.focusables = [
            self.btn_print,
            self.btn_if,
            self.btn_for,
            self.btn_def,
            self.btn_while,
            *self.keyboard_buttons,
            self.btn_run,
            self.btn_clear_output,
            self.btn_back
        ]

    # ================= BUTTON FACTORY =================
    def _create_button(self, text, layout):

        btn = TestButton(text, self)
        btn.setMinimumSize(200,60)

        layout.addWidget(btn)

        return btn

    # ================= INSERT TEXT =================
    def insert_text(self, text):

        cursor = self.editor.textCursor()
        cursor.insertText(text)

        self.editor.setTextCursor(cursor)
        self.editor.setFocus()

    # ================= RUN CODE =================
    def run_code(self):

        code = self.editor.toPlainText()

        if not code.strip():
            self.output_console.setPlainText("No code to execute.")
            return

        try:
            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".py",
                mode="w",
                encoding="utf-8"
            ) as temp_file:

                temp_file.write(code)
                temp_path = temp_file.name

            result = subprocess.run(
                ["python", temp_path],
                capture_output=True,
                text=True,
                timeout=3
            )

            output = result.stdout + result.stderr

            if not output:
                output = "Program executed successfully."

            self.output_console.setPlainText(output)

        except subprocess.TimeoutExpired:
            self.output_console.setPlainText("Execution timed out.")

        except Exception as e:
            self.output_console.setPlainText(f"Error:\n{str(e)}")

    # ================= CLEAR OUTPUT =================
    def clear_output(self):
        self.output_console.clear()

    # ================= HANDLE SNIPPETS =================
    def handle_snippet(self, button):

        if button in self.snippet_map:
            self.insert_text(self.snippet_map[button])

    # ================= BACK =================
    def go_back(self):

        self.main_window.switch_state(AppState.HOME)