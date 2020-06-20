# -*- coding: UTF-8 -*-
from PyQt5 import QtGui
from PyQt5.QtCore import QRect, Qt, QDir
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
import sys
import os

from TkPy3.default_configs import get_configs
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
        self.config_view = QStackedWidget()
        self.get_start()

    def get_start(self):
        self.setMinimumHeight(300)
        self.setMinimumWidth(600)
        self.resize(860, 400)
        self.hbox.addWidget(self.config_list)
        self.hbox.addWidget(self.config_view)
        self.config_list.currentRowChanged.connect(self.diaplay_config_list)
        self.setLayout(self.hbox)
        self.config_view.addWidget(self.init_base_config())
        self.config_list.addItem('基础设置')
        self.config_view.addWidget(self.init_style_config())
        self.config_list.addItem('样式设置')

    def init_base_config(self):
        widget = QWidget()
        return widget

    def init_style_config(self):
        widget = QWidget()
        layout = QFormLayout()
        widget.setLayout(layout)
        style_list = QComboBox()
        complete = QCompleter(QStyleFactory.keys())
        complete.setFilterMode(Qt.MatchContains)
        complete.setCompletionMode(QCompleter.PopupCompletion)
        style_list.setCompleter(complete)
        style_list.setEditable(True)
        style_list.addItems(QStyleFactory.keys())
        layout.addRow('选择样式: ', style_list)
        return widget

    def diaplay_config_list(self, index):
        self.config_view.setCurrentIndex(index)


def main():
    app = QApplication(sys.argv)
    dialog = ConfigDialog()
    sys.exit(dialog.exec_())


if __name__ == '__main__':
    main()
