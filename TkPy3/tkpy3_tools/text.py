# -*- coding: UTF-8 -*-
import os
import sys

import jedi
from PyQt5.Qsci import QsciAPIs, QsciScintilla
from PyQt5.QtGui import QColor, QContextMenuEvent
from PyQt5.QtCore import pyqtSignal, Qt, QThread
from PyQt5.QtWidgets import QApplication, QTextBrowser, QMenu, QAction
from diff_match_patch import diff_match_patch
from pygments.token import Name

from TkPy3.locale_dirs import BASE_DIR
from TkPy3.tkpy3_tools.PyQt5_tools import RGB
from TkPy3.tkpy3_tools.events import get_event
from TkPy3.tkpy3_tools.lexers import TkPyPythonLexer
from TkPy3.tkpy3_tools.start import set_icon_to_tkpy3, tkpy3_setup


class PythonLexer(TkPyPythonLexer):
    def __init__(self, parent):
        super(PythonLexer, self).__init__(parent)
        editor = self.parent()
        editor.SendScintilla(editor.SCI_STYLESETHOTSPOT, 1, True)


text_lexer = PythonLexer


def assert_text(old_text, new_text):
    dmp = diff_match_patch()
    patches = dmp.patch_make(old_text, new_text)
    diff = dmp.patch_toText(patches)

    patches = dmp.patch_fromText(diff)
    new_text, _ = dmp.patch_apply(patches, old_text)
    return bool(_)


def view_license():
    widget = QTextBrowser()
    widget.setLineWrapMode(0)
    set_icon_to_tkpy3(widget)
    widget.resize(800, 550)
    with open(os.path.join(BASE_DIR, 'LICENSE.txt')) as f:
        widget.setPlainText(f.read())
    widget.setWindowTitle('TkPy3 License')
    return widget


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
                print(script.completions(True)[0].description)
            for completion in script.completions(True):
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
    format_code = pyqtSignal()
    sort_imports = pyqtSignal()

    def __init__(self, parent=None):
        QsciScintilla.__init__(self, parent)
        self.complete = AutoComplete()
        self.complete.prepare.connect(self.update_completes)
        self.lexer = text_lexer(self)
        self.setLexer(self.lexer)
        self.api = QsciAPIs(self.lexer)
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
        self.autoCompleteFromAll()
        self.setAutoCompletionThreshold(1)
        self.setAutoCompletionSource(QsciScintilla.AcsAll)
        self.setUtf8(True)
        self.setBraceMatching(QsciScintilla.StrictBraceMatch)
        self.setMatchedBraceForegroundColor(QColor(self.lexer.styles[Name.Decorator]))
        self.setMatchedBraceBackgroundColor(RGB(0, 255, 0).to_pyqt_color())
        self.setCallTipsVisible(-1)

    def goto_html_or_define(self, position):
        print(position)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            if QApplication.keyboardModifiers() == Qt.ControlModifier:
                self.autoCompleteFromAll()
                return
        QsciScintilla.keyPressEvent(self, event)
        self.complete.line, self.complete.column = self.getCursorPosition()
        self.complete.text = self.text()
        self.setMarginWidth(0, len(str(len(self.text().split('\n')))) * 20)
        # if event.key() not in [Qt.Key_Up, Qt.Key_Down, Qt.Key_Left, Qt.Key_Right]:
        #    if not self.complete.started:
        #        self.complete.start()
        self.key_pressed.emit()

    def contextMenuEvent(self, event: QContextMenuEvent) -> None:
        menu = QMenu(self)
        complete_code = menu.addAction('代码提示')
        complete_code.triggered.connect(self.autoCompleteFromAll)
        complete_code.setShortcut('Ctrl+Space')
        menu.addSeparator()
        copy = menu.addAction('复制')
        copy.setShortcut(get_event('Ctrl+C'))
        copy.triggered.connect(self.copy)
        paste = menu.addAction('粘贴')
        paste.setShortcut(get_event('Ctrl+V'))
        paste.triggered.connect(self.paste)
        cut = menu.addAction('剪切')
        cut.setShortcut(get_event('Ctrl+X'))
        cut.triggered.connect(self.cut)
        menu.addSeparator()
        undo = menu.addAction('撤销')
        undo.setShortcut(get_event('Ctrl+Z'))
        undo.triggered.connect(self.undo)
        redo = menu.addAction('撤回')
        redo.setShortcut('Ctrl+Y')
        redo.triggered.connect(self.redo)
        menu.addSeparator()
        format_code = menu.addAction('格式化代码')
        format_code.triggered.connect(self.format_code.emit)
        format_code.setShortcut('Ctrl+Alt+L')
        sort_imports = menu.addAction('整理Import语句')
        sort_imports.triggered.connect(self.sort_imports.emit)
        menu.exec_(event.globalPos())

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

    def goto_line(self, lineno: int, column: int = 0):
        self.setCursorPosition(lineno, column)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = TkPyTextEdit()
    tkpy3_setup(app)
    v = view_license()
    v.show()
    widget.resize(800, 600)
    widget.setWindowTitle('TkPy3 Test')
    widget.show()
    sys.exit(app.exec_())
