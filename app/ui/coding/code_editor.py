from PyQt6.QtWidgets import QPlainTextEdit
from PyQt6.QtGui import QTextCursor
from PyQt6.QtCore import Qt


class CodeEditor(QPlainTextEdit):

    def keyPressEvent(self, event):

        cursor = self.textCursor()

        pairs = {
            "(": ")",
            "[": "]",
            "{": "}",
            '"': '"',
            "'": "'"
        }

        # ---------- AUTO CLOSE BRACKETS ----------
        if event.text() in pairs:

            closing = pairs[event.text()]

            cursor.insertText(event.text() + closing)

            cursor.movePosition(QTextCursor.MoveOperation.Left)
            self.setTextCursor(cursor)

            return

        # ---------- AUTO INDENT ----------
        if event.key() == Qt.Key.Key_Return:

            cursor.select(QTextCursor.SelectionType.LineUnderCursor)
            line = cursor.selectedText()

            indent = ""

            for ch in line:
                if ch in [" ", "\t"]:
                    indent += ch
                else:
                    break

            super().keyPressEvent(event)

            cursor = self.textCursor()
            cursor.insertText(indent)

            if line.strip().endswith(":"):
                cursor.insertText("    ")

            return

        super().keyPressEvent(event)