from PyQt5.QtGui import QCloseEvent, QKeyEvent, QTextCursor
from PyQt5.QtWidgets import QWidget, QApplication, QTextEdit, QMessageBox, QVBoxLayout, QErrorMessage
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QMimeData

import sys
import platform
import code
import builtins

from TkPy3.tkpy3_tools.start import tkpy3_setup
from TkPy3.tkpy3_tools.gnu_gettext_extensions import _


class Shell(code.InteractiveConsole, QThread):
    input_text = pyqtSignal(str)
    output = pyqtSignal(str)
    start_input = pyqtSignal()
    end_input = pyqtSignal()
    close = pyqtSignal()
    input_res_text = None

    def __init__(self, global_locals=None, filename="stdout"):
        code.InteractiveConsole.__init__(self, global_locals, filename)
        QThread.__init__(self)

        def set_input_res_text(text: str):
            self.input_res_text = text

        self.input_text.connect(set_input_res_text)
        builtins.__dict__['input'] = self.raw_input
        sys.stdout.write = self.write
        sys.stderr.write = self.write
        sys.stdin.readline = lambda: self.raw_input()

    def run(self):
        self.interact()

    def interact(self, banner=None, exitmsg=None):
        try:
            sys.ps1
        except AttributeError:
            sys.ps1 = ">>> "
        try:
            sys.ps2
        except AttributeError:
            sys.ps2 = "... "
        cprt = 'Type "help", "copyright", "credits" or "license" for more information.\n'
        if banner is None:
            self.write("Python %s" % sys.version + '\n%s' % cprt)
        elif banner:
            self.write("%s\n" % str(banner))
        more = 0
        while 1:
            try:
                if more:
                    prompt = sys.ps2
                else:
                    prompt = sys.ps1
                try:
                    line = self.raw_input(prompt)
                except EOFError:
                    self.write("\n")
                    break
                else:
                    more = self.push(line)
            except KeyboardInterrupt:
                self.write("\nKeyboardInterrupt\n")
                self.resetbuffer()
                more = 0
            except SystemExit:
                self.close.emit()
                self.resetbuffer()
                more = 0
        if exitmsg is None:
            self.write('')
        elif exitmsg != '':
            self.write('%s\n' % exitmsg)

    def raw_input(self, prompt=""):
        self.output.emit(prompt)
        self.start_input.emit()
        while not self.input_res_text:
            pass
        text = self.input_res_text[len(prompt):]
        self.input_res_text = None
        self.end_input.emit()
        return text

    def write(self, data: str):
        self.output.emit(data)

    def showsyntaxerror(self, filename: str):
        self.write('Traceback (most recent call last):\n')
        code.InteractiveConsole.showsyntaxerror(self, filename)

    def showtraceback(self):
        self.write('Traceback (most recent call last):\n')
        code.InteractiveConsole.showtraceback(self)


class ShellText(QTextEdit):
    line = pyqtSignal(str)
    KeyboardInterrupt = pyqtSignal()
    input_open = False
    min_char = 0

    def __init__(self, parent=None):
        QTextEdit.__init__(self, parent)
        self.__insert_one_line = False

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key_Return and self.input_open:
            text = self.toPlainText()
            line = text.split('\n')[-1]
            self.line.emit(line)
            cursor = self.textCursor()
            cursor.movePosition(QTextCursor.End)
            self.setTextCursor(cursor)
            QTextEdit.keyPressEvent(self, event)
        elif event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_C:
            if not self.textCursor().selectedText():
                self.RaiseKeyboardInterrupt()
            else:
                self.copy()
        elif event.key() in [Qt.Key_Backspace, Qt.Key_Delete]:
            if self.textCursor().position() - 1 >= self.min_char:
                QTextEdit.keyPressEvent(self, event)
        else:
            QTextEdit.keyPressEvent(self, event)

    def RaiseKeyboardInterrupt(self):
        self.KeyboardInterrupt.emit()

    def insertPlainText(self, text: str) -> None:
        self.min_char += len(text)
        QTextEdit.insertPlainText(self, text)

    def setInputOpen(self, b: bool):
        self.input_open = b

    def insertFromMimeData(self, source: QMimeData) -> None:
        if source.hasText():
            self.textCursor().insertText(source.text())


class TkPyShell(QWidget):
    close_sub_window = pyqtSignal()

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setWindowTitle(f'PyShell (Python {platform.python_version()})')
        self.__layout = QVBoxLayout()
        self.text = ShellText()
        self.shell = Shell()
        self.shell.start()
        self.shell.output.connect(lambda text: self.text.insertPlainText(text))
        self.shell.start_input.connect(lambda: self.text.setInputOpen(True))
        self.text.line.connect(self.shell.input_text.emit)
        self.shell.end_input.connect(lambda: self.text.setInputOpen(False))
        self.shell.close.connect(self.close)
        self.setLayout(self.__layout)
        self.__layout.addWidget(self.text)

    def closeEvent(self, event: QCloseEvent) -> None:
        res = QMessageBox.question(self, _('问题'), _('是否退出PyShell?这将会结束这个Shell进程。'))
        if res == QMessageBox.Yes:
            self.shell.terminate()
            self.close_sub_window.emit()
            event.accept()
        else:
            event.ignore()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    tkpy3_setup(app)
    shell = TkPyShell()
    shell.show()
    sys.exit(app.exec_())
