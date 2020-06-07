# -*- coding: UTF-8 -*-
import sys
import os

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from TkPy3.version import version as tkpy_version
from TkPy3.locale_dirs import images_icon_dir


class RelyDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.setWindowTitle(f'TkPy{tkpy_version} 依赖')
        self.setWindowIcon(QIcon(os.path.join(images_icon_dir, 'help_icons', 'tools.png')))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = RelyDialog()
    sys.exit(dialog.exec_())
