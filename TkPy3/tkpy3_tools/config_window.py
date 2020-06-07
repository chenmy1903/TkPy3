# -*- coding: UTF-8 -*-
from PyQt5 import QtGui
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
import sys
import os

from TkPy3.default_configs import get_configs, add_config
from TkPy3.locale_dirs import images_icon_dir
from pygments.styles import STYLE_MAP


def get_pygments_stylemap():
    pygments_stylemap = list(STYLE_MAP.keys())
    pygments_stylemap.remove(get_configs()['highlight_style'])
    pygments_stylemap.insert(0, get_configs()['highlight_style'])
    return pygments_stylemap


class ConfigDialog(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setWindowTitle('TkPy3设置')
        self.hbox = QHBoxLayout(self)
        self.setWindowIcon(QIcon(os.path.join(images_icon_dir, 'config_icons', 'advanced.png')))
        self.config_list = QListWidget()
        self.base_config = QWidget()
        self.config_view = QStackedWidget()
        self.get_start()

    def get_start(self):
        self.setMinimumHeight(300)
        self.setMinimumWidth(600)
        self.resize(860, 400)
        self.hbox.addWidget(self.config_list)
        self.hbox.addWidget(self.config_view)
        self.config_list.insertItem(0, '基础设置')
        self.config_view.addWidget(self.base_config)
        self.config_list.currentRowChanged.connect(self.diaplay_config_list)
        self.setLayout(self.hbox)
        self.init_base_config()

    def init_base_config(self):
        pass
        
    def diaplay_config_list(self, i):
        self.config_view.setCurrentIndex(i)

    def set_pygments_style(self):
        item = QInputDialog.getItem(self, 'Pygments高亮主题', '请选择Pygments高亮主题:', get_pygments_stylemap())
        add_config('highlight_style', item)


def main():
    app = QApplication(sys.argv)
    dialog = ConfigDialog()
    sys.exit(dialog.exec_())


if __name__ == '__main__':
    main()
