# -*- coding: UTF-8 -*-
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import *


class TkPyFindWidget(QWidget):
    pos = pyqtSignal([int, int])

    def __init__(self, parent=None):
        super(TkPyFindWidget, self).__init__(parent)
        QLabel(self).setText('<h1>123123123123</h1>')
