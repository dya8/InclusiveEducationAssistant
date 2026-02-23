import subprocess
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
        self.editor = QPlainTextEdit()
        self.editor.setPlaceholderText("Write your Python code here...")
        self.editor.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.editor.setFont(QFont("Consolas", 14))
        main_layout.addWidget(self.editor, stretch=2)

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
        main_layout.addWidget(self.output_console, stretch=2)

        # ================= CONTROL BUTTONS =================
        control_layout = QHBoxLayout()

        self.btn_run = self._create_button("RUN CODE", control_layout)
        self.btn_clear = self._create_button("CLEAR OUTPUT", control_layout)
        self.btn_back = self._create_button("BACK", control_layout)

        main_layout.addLayout(control_layout)

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
            self.btn_if: "if condition:\n\t",
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