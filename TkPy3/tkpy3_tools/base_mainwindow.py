# -*- coding: UTF-8 -*-
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal
import sys

from TkPy3.tkpy3_tools.editor import EditSubWindow
from TkPy3.tkpy3_tools.start import tkpy3_setup


class TkPyDockWidget(QDockWidget):
    close_window = pyqtSignal()
    open_window = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(TkPyDockWidget, self).__init__(*args, **kwargs)
        self.open_window.emit()

    def closeEvent(self, event: QCloseEvent):
        self.close_window.emit()
        return super(TkPyDockWidget, self).closeEvent(event)


class BaseTkPy3(QWidget):
    def __init__(self, parent=None):
        super(BaseTkPy3, self).__init__(parent)
        self.layout = QHBoxLayout()
        self.splitter = QSplitter()
        self.mdi = QMdiArea()
        self.mdi.setObjectName('WindowMdi')
        self.init_ui()

    def init_ui(self):
        self.setLayout(self.layout)
        self.splitter.addWidget(self.mdi)
        self.layout.addWidget(self.splitter, 0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    tkpy3_setup(app)
    tkpy3 = BaseTkPy3()
    window = EditSubWindow()
    window.resize(600, 600)
    window.setWindowTitle('TkPy3 Sub Window')
    tkpy3.mdi.addSubWindow(window)
    tkpy3.show()
    tkpy3.setWindowTitle('TkPy3 Test')
    sys.exit(app.exec_())
