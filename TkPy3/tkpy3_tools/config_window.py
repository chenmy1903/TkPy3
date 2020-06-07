# -*- coding: UTF-8 -*-
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
import sys
import os

from TkPy3.locale_dirs import images_icon_dir


class ConfigDialog(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setWindowTitle('TkPy3设置')
        self.setWindowIcon(QIcon(os.path.join(images_icon_dir, 'config_icons', 'advanced.png')))


def main():
    app = QApplication(sys.argv)
    dialog = ConfigDialog()
    sys.exit(dialog.exec_())


if __name__ == '__main__':
    main()
