# -*- coding: UTF-8 -*-
import sys
# from PyQt5.Qt import PYQT_VERSION_STR
from PyQt5.QtWidgets import *
# from TkPy3.version import version as tkpy_version
import platform
import textwrap


def about_qt(parent=QWidget()):
    QMessageBox.aboutQt(parent, '关于Qt')


def about_tkpy3(parent=QWidget()):
    QMessageBox.information(parent, '关于TkPy3', """
    TkPy3一个使用PyQt5制作的TkPy IDE
    TkPy3: 
    PyQt5: 
    System:     
    """)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    about_tkpy3()
    sys.exit(app.exec_())
