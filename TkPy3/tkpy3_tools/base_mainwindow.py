# -*- coding: UTF-8 -*-
from PyQt5.QtWidgets import *
import sys


class BaseTkPy3(QWidget):
    def __init__(self, parent=None):
        super(BaseTkPy3, self).__init__(parent)
        self.layout = QHBoxLayout()
        self.mdi = QMdiArea()
        self.mdi.setObjectName('WindowMdi')
        self.init_ui()

    def init_ui(self):
        self.setLayout(self.layout)
        self.layout.addWidget(self.mdi, 0)
