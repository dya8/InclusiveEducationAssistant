'''from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
    QStackedLayout
)

from PyQt6.QtGui import QFont, QTextOption
from PyQt6.QtCore import Qt
import sys
from app.ui.coding.coding_template import CodingTemplates
from app.ui.coding.coding_keyboard import CodingKeyboard
from app.ui.coding.coding_controls import CodingControls
from app.ui.coding.coding_keybutton import CodingKeyButton
from app.ui.coding.code_editor import CodeEditor
from core.input.input_events import Action

import subprocess
import tempfile


class CodingScreen(QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # ---------------- TITLE ----------------

        title = QLabel("Assistive Coding - Python")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size:20px;font-weight:bold;")

        main_layout.addWidget(title)

        # ---------------- TOP AREA ----------------

        top_layout = QHBoxLayout()
        main_layout.addLayout(top_layout)

        # -------- CODE EDITOR --------

        self.editor = CodeEditor(self)
        #self.editor.setFont(QFont("Consolas", 14))
        #self.editor.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        #self.editor.setWordWrapMode(QTextOption.WrapMode.NoWrap)

        top_layout.addWidget(self.editor, 2)

        # -------- OUTPUT CONSOLE --------

        self.output_console = QPlainTextEdit()
        self.output_console.setReadOnly(True)
        self.output_console.setFont(QFont("Consolas", 12))

        self.output_console.setStyleSheet(
            "background-color:#1e1e1e;color:#00ff00;"
        )

        top_layout.addWidget(self.output_console, 1)

        # ---------------- BOTTOM AREA ----------------

        bottom_layout = QHBoxLayout()
        main_layout.addLayout(bottom_layout)

        # -------- LEFT PANEL (TEMPLATES / KEYBOARD) --------

        self.panel_container = QWidget()
        self.panel_stack = QStackedLayout()

        self.panel_container.setLayout(self.panel_stack)

        bottom_layout.addWidget(self.panel_container, 2)

        # Panels
        self.templates = CodingTemplates(self)
        self.keyboard = CodingKeyboard(self)

        self.panel_stack.addWidget(self.templates)
        self.panel_stack.addWidget(self.keyboard)

        # default
        self.panel_stack.setCurrentWidget(self.templates)

        # -------- RIGHT CONTROLS --------

        self.controls = CodingControls(self)
        bottom_layout.addWidget(self.controls, 1)

        # ---------------- CONTROL BUTTONS ----------------

        control_layout = QHBoxLayout()
        main_layout.addLayout(control_layout)

        self.btn_run = CodingKeyButton(
            "Run Code",
            Action.RUN_CODE,
            None,
            self
        )

        self.btn_clear = CodingKeyButton(
            "Clear Output",
            Action.CLEAR_OUTPUT,
            None,
            self
        )

        self.btn_back = CodingKeyButton(
            "Back",
            Action.BACK,
            None,
            self
        )

        control_layout.addWidget(self.btn_run)
        control_layout.addWidget(self.btn_clear)
        control_layout.addWidget(self.btn_back)

        # ---------------- FOCUSABLES ----------------

        self.focusables = []

        self.update_focusables()

    # ---------------- FOCUSABLE UPDATE ----------------

    def update_focusables(self):

        panel = self.panel_stack.currentWidget()

        self.focusables = (
            panel.focusables
            + self.controls.focusables
            + [self.btn_run, self.btn_clear, self.btn_back]
        )

    # ---------------- PANEL SWITCH ----------------

    def show_templates(self):

        self.panel_stack.setCurrentWidget(self.templates)
        self.update_focusables()

    def show_keyboard(self):

        self.panel_stack.setCurrentWidget(self.keyboard)
        self.update_focusables()

    # ---------------- TEXT INSERT ----------------

    def insert_text(self, text):

        cursor = self.editor.textCursor()
        cursor.insertText(text)

        self.editor.setTextCursor(cursor)

    # ---------------- BACKSPACE ----------------

    def backspace(self):

        cursor = self.editor.textCursor()
        cursor.deletePreviousChar()

        self.editor.setTextCursor(cursor)

    # ---------------- RUN CODE ----------------

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
                [sys.executable, temp_path],
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

            self.output_console.setPlainText(str(e))

    # ---------------- CLEAR OUTPUT ----------------

    def clear_output(self):

        self.output_console.clear()

    def show_main(self):
        self.panel_stack.setCurrentWidget(self.main_panel)'''

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
    QStackedLayout
)

from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
import sys
import subprocess
import tempfile

from app.ui.coding.coding_template import CodingTemplates
from app.ui.coding.coding_keyboard import CodingKeyboard
from app.ui.coding.coding_controls import CodingControls
from app.ui.coding.coding_keybutton import CodingKeyButton
from app.ui.coding.code_editor import CodeEditor

from core.input.input_events import Action


class CodingScreen(QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # ---------------- TITLE ----------------

        title = QLabel("Assistive Coding - Python")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size:20px;font-weight:bold;")

        main_layout.addWidget(title)

        # ---------------- TOP AREA ----------------

        top_layout = QHBoxLayout()
        main_layout.addLayout(top_layout)

        # -------- CODE EDITOR --------

        self.editor = CodeEditor(self)
        top_layout.addWidget(self.editor, 2)

        # -------- OUTPUT CONSOLE --------

        self.output_console = QPlainTextEdit()
        self.output_console.setReadOnly(True)
        self.output_console.setFont(QFont("Consolas", 12))
        self.output_console.setStyleSheet(
            "background-color:#1e1e1e;color:#00ff00;"
        )

        top_layout.addWidget(self.output_console, 1)

        # ---------------- BOTTOM AREA ----------------

        bottom_layout = QHBoxLayout()
        main_layout.addLayout(bottom_layout)

        # -------- LEFT PANEL (STACKED) --------

        self.panel_container = QWidget()
        self.panel_stack = QStackedLayout()
        self.panel_container.setLayout(self.panel_stack)

        bottom_layout.addWidget(self.panel_container, 2)

        # ================= MAIN PANEL =================

        self.main_panel = QWidget()
        main_panel_layout = QVBoxLayout()

        self.btn_templates = CodingKeyButton(
            "Templates",
            Action.OPEN_TEMPLATES,
            None,
            self
        )

        self.btn_keyboard = CodingKeyButton(
            "Keyboard",
            Action.OPEN_CKEYBOARD,
            None,
            self
        )

        main_panel_layout.addWidget(self.btn_templates)
        main_panel_layout.addWidget(self.btn_keyboard)

        self.main_panel.setLayout(main_panel_layout)

        # ================= OTHER PANELS =================

        self.templates = CodingTemplates(self)
        self.keyboard = CodingKeyboard(self)

        # Add panels to stack
        self.panel_stack.addWidget(self.main_panel)
        self.panel_stack.addWidget(self.templates)
        self.panel_stack.addWidget(self.keyboard)

        # Default panel
        self.panel_stack.setCurrentWidget(self.main_panel)

        # -------- RIGHT CONTROLS --------

        self.controls = CodingControls(self)
        bottom_layout.addWidget(self.controls, 1)

        # ---------------- CONTROL BUTTONS ----------------

        control_layout = QHBoxLayout()
        main_layout.addLayout(control_layout)

        self.btn_run = CodingKeyButton(
            "Run Code",
            Action.RUN_CODE,
            None,
            self
        )

        self.btn_clear = CodingKeyButton(
            "Clear Output",
            Action.CLEAR_OUTPUT,
            None,
            self
        )

        self.btn_back = CodingKeyButton(
            "Back",
            Action.BACK,
            None,
            self
        )

        control_layout.addWidget(self.btn_run)
        control_layout.addWidget(self.btn_clear)
        control_layout.addWidget(self.btn_back)

        # ---------------- FOCUSABLES ----------------

        self.focusables = []
        self.update_focusables()

    # ---------------- UPDATE FOCUSABLES ----------------

    def update_focusables(self):

        panel = self.panel_stack.currentWidget()

        if panel == self.main_panel:
            self.focusables = [
                self.btn_templates,
                self.btn_keyboard
            ]

        else:
            self.focusables = panel.focusables

        self.focusables += (
            self.controls.focusables +
            [self.btn_run, self.btn_clear, self.btn_back]
        )

    # ---------------- PANEL SWITCH ----------------

    def show_main(self):

        self.panel_stack.setCurrentWidget(self.main_panel)
        self.update_focusables()

    def show_templates(self):

        self.panel_stack.setCurrentWidget(self.templates)
        self.update_focusables()

    def show_keyboard(self):

        self.panel_stack.setCurrentWidget(self.keyboard)
        self.update_focusables()

    # ---------------- TEXT INSERT ----------------

    def insert_text(self, text):

        cursor = self.editor.textCursor()
        cursor.insertText(text)
        self.editor.setTextCursor(cursor)

    # ---------------- BACKSPACE ----------------

    def backspace(self):

        cursor = self.editor.textCursor()
        cursor.deletePreviousChar()
        self.editor.setTextCursor(cursor)

    # ---------------- RUN CODE ----------------

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
                [sys.executable, temp_path],
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
            self.output_console.setPlainText(str(e))

    # ---------------- CLEAR OUTPUT ----------------

    def clear_output(self):

        self.output_console.clear()
