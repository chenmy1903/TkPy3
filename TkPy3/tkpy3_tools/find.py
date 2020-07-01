# -*- coding: UTF-8 -*-
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget


class TkPyFindWidget(QWidget):
    pos = pyqtSignal([int, int])

    def __init__(self, parent=None):
        super(TkPyFindWidget, self).__init__(parent)
