# -*- coding: UTF-8 -*-
import os
import sys

from PyQt5 import QtGui

from TkPy3.default_configs import add_diff, get_configs
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *

from TkPy3.tkpy3_tools.editor import BaseEditor

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        add_diff()
        self.not_save_list = []
        self.setWindowTitle(get_configs()['init_title'])
        self.setWindowIcon(QIcon(get_configs()['init_icon_path']))
        self.edit = BaseEditor(self)
        self.setCentralWidget(self.edit)
        self.Menu: QMenuBar = self.menuBar()
        self.FileMenu = self.Menu.addMenu('文件')
        self.EditMenu = self.Menu.addMenu('编辑')
        self.SelectMenu = self.Menu.addMenu('选择')
        self.ViewMenu = self.Menu.addMenu('查看')
        self.GoToMenu = self.Menu.addMenu('转到')
        self.RunMenu = self.Menu.addMenu('运行')
        self.TermMenu = self.Menu.addMenu('终端')
        self.HelpMenu = self.Menu.addMenu('帮助')
        self.get_start()

    def get_start(self):
        self.edit.move(500, 500)

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        if self.not_save_list:
            res = QMessageBox.question(self, 'TkPy3 - 问题', '还有文件未保存？是否退出保存之后TkPy3？',
                                       QMessageBox.Ok | QMessageBox.No | QMessageBox.Cancel,
                                       QMessageBox.Cancel)
            if res == QMessageBox:
                self.save_files()
                event.accept()
            elif res == QMessageBox.No:
                event.accept()
            elif res == QMessageBox.Cancel:
                event.ignore()

    def save_files(self):
        pass


def main():
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
