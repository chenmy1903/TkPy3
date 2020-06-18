# -*- coding: UTF-8 -*-
import os
import sys

import jedi
from PyQt5.Qsci import QsciAPIs, QsciLexerPython, QsciScintilla
from PyQt5.QtGui import QColor
from PyQt5.QtCore import pyqtSignal, Qt, QThread
from PyQt5.QtPrintSupport import QPrintDialog
from PyQt5.QtWidgets import QApplication
from diff_match_patch import diff_match_patch

from TkPy3 import get_configs
from TkPy3.locale_dirs import PYQT5_PATH


def assert_text(old_text, new_text):
    dmp = diff_match_patch()
    patches = dmp.patch_make(old_text, new_text)
    diff = dmp.patch_toText(patches)

    patches = dmp.patch_fromText(diff)
    new_text, _ = dmp.patch_apply(patches, old_text)
    return bool(_)


class AutoComplete(QThread):
    prepare = pyqtSignal(list, tuple)
    started: bool = False
    line: int
    column: int
    text: str

    def run(self):
        completions = []
        self.started = True
        line, column = self.line, self.column
        if line and column:
            script = jedi.Script(
                self.text, line + 1, column)
            if script.completions():
                print(script.completions()[0].description)
            for completion in script.completions():
                completions.append(completion.name)
        self.prepare.emit(completions)
        self.started = False


def get_eol_mode(mode: str):
    mode = mode.lower()
    if mode == 'windows':
        return QsciScintilla.EolWindows
    elif mode == 'unix':
        return QsciScintilla.EolUnix
    elif mode == 'mac':
        return QsciScintilla.EolMac


class TkPyTextEdit(QsciScintilla):
    key_pressed = pyqtSignal()

    def __init__(self, parent=None):
        QsciScintilla.__init__(self, parent)
        self.complete = AutoComplete()
        self.complete.prepare.connect(self.update_completes)
        self.lexer = QsciLexerPython(self)
        self.setLexer(self.lexer)
        self.api = QsciAPIs(self.lexer)
        self.api.load(os.path.join(PYQT5_PATH, "Qt/qsci/api/python/PyQt5.api"))
        self.setAutoIndent(True)
        self.setMarginLineNumbers(0, True)
        self.setEdgeMode(QsciScintilla.EdgeLine)
        self.setEdgeColumn(79)
        self.setEdgeColor(QColor(0, 0, 0))
        """
        self.setIndentationsUseTabs(True)
        self.setIndentationWidth(get_configs()['tab_width'])
        self.setTabWidth(get_configs()['tab_width'])
        self.setTabIndents(get_configs()['indent_with_tabs'])
        self.setBackspaceUnindents(True)
        self.setCaretLineVisible(True)
        self.setIndentationGuides(True)
        self.setCaretForegroundColor(QColor(get_configs()['cursor_color']))
        self.setCaretLineBackgroundColor(QColor(get_configs()['line_background_color']))
        self.setCaretWidth(6)
        self.setWrapMode(QsciScintilla.WrapNone if not get_configs()['text_wrap'] else QsciScintilla.WrapWhitespace)
        self.setEolMode(get_eol_mode(get_configs()['eol_mode']))
        # self.setMarginsForegroundColor(QColor("#ff888888"))
        """
        self.setMarginWidth(0, len(str(len(self.text().split('\n')))) * 20)
        self.setFolding(QsciScintilla.PlainFoldStyle)
        self.setAutoCompletionSource(QsciScintilla.AcsAll)
        self.setAutoCompletionCaseSensitivity(True)
        self.setAutoCompletionReplaceWord(True)
        self.autoCompleteFromDocument()
        self.setAutoCompletionThreshold(1)
        self.setAutoCompletionSource(QsciScintilla.AcsAll)
        self.setUtf8(True)
        self.setCallTipsVisible(-1)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            if QApplication.keyboardModifiers() == Qt.ControlModifier:
                self.autoCompleteFromDocument()
                return
        QsciScintilla.keyPressEvent(self, event)
        self.complete.line, self.complete.column = self.getCursorPosition()
        self.complete.text = self.text()
        self.setMarginWidth(0, len(str(len(self.text().split('\n')))) * 20)
        # if event.key() not in [Qt.Key_Up, Qt.Key_Down, Qt.Key_Left, Qt.Key_Right]:
        #    if not self.complete.started:
        #        self.complete.start()
        self.key_pressed.emit()

    def paste(self):
        QsciScintilla.paste(self)
        self.key_pressed.emit()
        self.setMarginWidth(0, len(str(len(self.text().split('\n')))) * 20)

    def cut(self):
        QsciScintilla.cut(self)
        self.key_pressed.emit()
        self.setMarginWidth(0, len(str(len(self.text().split('\n')))) * 20)

    def update_completes(self, completes):
        for complete in completes:
            self.api.add(complete)
        self.api.prepare()


if __name__ == "__main__":
    app = QApplication([])
    widget = TkPyTextEdit()
    widget.resize(800, 600)
    widget.setWindowTitle('TkPy3 Test')
    widget.show()
    sys.exit(app.exec_())
