from PyQt5.QtWidgets import *
import sys
from PyQt5.QtCore import pyqtSignal, Qt

from TkPy3.tkpy3_tools.start import setup as tkpy_setup


class TkPyShell(QWidget):
    def __init__(self, parent=None):
        super(TkPyShell, self).__init__(parent)
        self.init_ui()

    def init_ui(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    tkpy_setup(app)
    shell = TkPyShell()
    shell.show()
    sys.exit(app.exec_())
