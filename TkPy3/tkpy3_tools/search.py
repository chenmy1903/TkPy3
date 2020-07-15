from PyQt5.QtGui import QIcon, QMouseEvent, QFocusEvent
from PyQt5.QtWidgets import QLineEdit, QApplication

from TkPy3.locale_dirs import pixmaps
from TkPy3.tkpy3_tools.gnu_gettext_extensions import _

import sys

from TkPy3.tkpy3_tools.start import tkpy3_setup


class SearchWidget(QLineEdit):
    def __init__(self, parent=None):
        QLineEdit.__init__(self, parent)
        self.setPlaceholderText(_('搜索'))
        self.addAction(QIcon(pixmaps["search"]), QLineEdit.LeadingPosition)
        self.setFrame(False)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.setPlaceholderText(_(''))
        return QLineEdit.mousePressEvent(self, event)

    def focusOutEvent(self, event: QFocusEvent) -> None:
        self.setPlaceholderText(_('搜索'))
        return QLineEdit.focusOutEvent(self, event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    tkpy3_setup(app)
    widget = SearchWidget()
    widget.setWindowTitle(_('搜索'))
    widget.show()
    sys.exit(app.exec_())
