from PyQt5.Qsci import QsciLexerPython
from PyQt5.QtGui import QColor
from pygments.token import Keyword, Name, Number, String, Comment, Error, Operator
from pygments.lexers.python import PythonLexer
from pygments.styles import get_style_by_name

from TkPy3 import get_configs
from TkPy3.tkpy3_tools.core import gen_style


class TkPyPythonLexer(QsciLexerPython):
    filenames = PythonLexer.filenames
    style = get_style_by_name(get_configs()['highlight_style'])
    selection = style.highlight_color
    background_color = style.background_color
    styles = gen_style(style.styles)

    def __init__(self, parent):
        super(TkPyPythonLexer, self).__init__(parent)
        self.setColor(QColor(self.styles[Name.Class]), self.ClassName)
        self.setColor(QColor(self.styles[Number]), self.Number)
        self.setColor(QColor(self.styles[String]), self.DoubleQuotedString)
        self.setColor(QColor(self.styles[Comment]), self.Comment)
        self.setColor(QColor(self.styles[Comment]), self.CommentBlock)
        self.setColor(QColor(self.styles[Keyword]), self.Keyword)
        self.setColor(QColor(self.styles[Name.Function]), self.FunctionMethodName)
        self.setColor(QColor(self.styles[Error]), self.UnclosedString)
        self.setColor(QColor(self.styles[String.Doc]), self.TripleDoubleQuotedString)
        self.setColor(QColor(self.styles[Operator]), self.Operator)
