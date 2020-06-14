from PyQt5.QtWidgets import *
import os
import sys
from PyQt5.QtCore import pyqtSlot
from multiprocessing import Process


class TkPyShell(QWidget):
    pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    shell = TkPyShell()
    shell.show()
    sys.exit(app.exec_())
