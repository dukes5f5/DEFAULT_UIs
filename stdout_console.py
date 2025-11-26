# stdout_console.py
import sys
from PyQt5.QtCore import QObject
from PyQt5.QtGui import QTextCursor

class _TextEditStream(QObject):
    def __init__(self, text_edit, override_color=None):
        super().__init__()
        self.text_edit = text_edit
        self.override_color = override_color

    def write(self, text):
        if not text.strip():
            return
        clean = text.strip()
        cursor = self.text_edit.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(clean + "\n")
        self.text_edit.setTextCursor(cursor)
        self.text_edit.ensureCursorVisible()

        if self.override_color:
            self.text_edit.setStyleSheet(f"color: {self.override_color};")

    def flush(self):
        pass

class StdoutConsole:
    def __init__(self, text_edit_widget):
        self.text_edit = text_edit_widget
        self._original_stdout = sys.stdout
        self._original_stderr = sys.stderr

        self.stdout_stream = _TextEditStream(self.text_edit)
        self.stderr_stream = _TextEditStream(self.text_edit, override_color="#FF5555")

        sys.stdout = self.stdout_stream
        sys.stderr = self.stderr_stream

    def restore(self):
        sys.stdout = self._original_stdout
        sys.stderr = self._original_stderr