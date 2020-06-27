from PyQt5.QtWidgets import *
import sys
import platform

from TkPy3.tkpy3_tools.start import setup as tkpy_setup


class TkPyShell(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setWindowTitle(f'PyShell (Python {platform.python_version()})')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    tkpy_setup(app)
    shell = TkPyShell()
    shell.show()
    sys.exit(app.exec_())
