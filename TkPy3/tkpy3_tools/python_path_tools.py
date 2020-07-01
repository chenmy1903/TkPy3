# -*- coding: UTF-8 -*-
import os
import sys

from PyQt5.QtGui import QIcon

from TkPy3.default_configs import add_config, get_configs
from TkPy3.locale_dirs import BASE_DIR
from PyQt5.QtWidgets import QDialog, QGridLayout, QListWidget, QApplication


class PathDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.layout = QGridLayout()
        self.path = sys.path
        self.ListBox = QListWidget()
        self.init_ui()

    def init_ui(self):
        self.setLayout(self.layout)

    def apply_path(self):
        sys.path = self.path


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = PathDialog()
    dialog.setWindowIcon(
        QIcon(os.path.join(BASE_DIR, "images", "icons", "python.png")))
    dialog.setWindowTitle('Python Path 管理器')
    dialog.show()
    sys.exit(app.exec_())
