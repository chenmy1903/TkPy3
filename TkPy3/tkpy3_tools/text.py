# -*- coding: UTF-8 -*-
from PyQt5.Qsci import QsciScintilla, QsciLexerPython, QsciLexerMarkdown
from PyQt5.QtGui import QColor
from diff_match_patch import diff_match_patch

from TkPy3 import get_configs


def assert_text(old_text, new_text):
    dmp = diff_match_patch()
    patches = dmp.patch_make(old_text, new_text)
    diff = dmp.patch_toText(patches)

    patches = dmp.patch_fromText(diff)
    new_text, _ = dmp.patch_apply(patches, old_text)
    return bool(_)


def get_eol_mode(mode: str):
    mode = mode.lower()
    if mode == 'windows':
        return QsciScintilla.EolWindows
    elif mode == 'unix':
        return QsciScintilla.EolUnix
    elif mode == 'mac':
        return QsciScintilla.EolMac


class TkPyTextEdit(QsciScintilla):
    def __init__(self, parent=None):
        QsciScintilla.__init__(self, parent)
        self.setIndentationsUseTabs(True)
        self.setIndentationWidth(get_configs()['tab_width'])
        self.setTabWidth(get_configs()['tab_width'])
        self.setTabIndents(get_configs()['indent_with_tabs'])
        self.setAutoIndent(True)
        # self.setBackspaceUnindents(True)
        # self.setCaretLineVisible(True)
        self.setIndentationGuides(True)
        # self.setEdgeMode(QsciScintilla.EdgeLine)
        # self.setEdgeColumn(80)
        # self.setEdgeColor(QColor(0, 0, 0))
        self.setLexer(QsciLexerPython(self))
        self.setMarginsForegroundColor(QColor("#ff888888"))
        self.setCaretForegroundColor(QColor(get_configs()['cursor_color']))
        # self.setCaretLineVisible(True)
        self.setCaretLineBackgroundColor(QColor(get_configs()['line_background_color']))
        self.setCaretWidth(6)
        self.setWrapMode(QsciScintilla.WrapNone if not get_configs()['text_wrap'] else QsciScintilla.WrapWhitespace)
        self.setEolMode(get_eol_mode(get_configs()['eol_mode']))
        self.setMarginsForegroundColor(QColor("#ff888888"))
        self.setUtf8(True)

