# -*- coding: UTF-8 -*-
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import *
from TkPy3.locale_dirs import BASE_DIR
import sys
import os

from TkPy3.tkpy3_tools.start import tkpy3_setup

load_dir = os.path.join(BASE_DIR, 'tkpy3_tools', 'qt_load')
images_dir = os.path.join(load_dir, 'images')


class LoadWidget(QLabel):
    def __init__(self, parent=None):
        super(LoadWidget, self).__init__(parent)
        self.load_gif = QMovie(os.path.join(images_dir, 'loading.gif'))
        self.setStyleSheet('background: black; color: white')
        self.init_ui()

    def init_ui(self):
        self.setMovie(self.load_gif)
        # self.setScaledContents(True)
        self.load_gif.start()
        self.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    tkpy3_setup(app)
    widget = LoadWidget()
    widget.setWindowTitle('TkPy3 Test - Loading... ...')
    widget.show()
    sys.exit(app.exec_())
