from PyQt5.QtWidgets import QApplication, QDialog, QFileDialog, QTableWidget, QLineEdit, QGridLayout
import sys
from TkPy3.tkpy3_tools.start import tkpy3_setup


class I18nDialog(QDialog):

    def __init__(self):
        QDialog.__init__(self)
        self.setWindowTitle('TkPy I18n Editor')
        self.__layout = QGridLayout()
        self.__init_ui()

    def __init_ui(self):
        self.setLayout(self.__layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    tkpy3_setup(app)
    dialog = I18nDialog()
    sys.exit(dialog.exec_())
