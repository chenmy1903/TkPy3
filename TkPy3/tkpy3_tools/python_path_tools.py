# -*- coding: UTF-8 -*-
import os
import sys

from PyQt5.QtGui import QIcon

from TkPy3.default_configs import add_config, get_configs
from TkPy3.locale_dirs import BASE_DIR
from PyQt5.QtWidgets import *


class PathWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.path_list = get_configs()['TkPy3_path']
        self.layout = QHBoxLayout()
        self.view_table = QTableWidget()
        self.get_start()

    def get_start(self):
        self.layout.addWidget(self.view_table)
        self.view_table.setColumnCount(1)
        self.view_table.setRowCount(len(self.path_list))
        self.add_paths()
        self.view_table.setHorizontalHeaderLabels(['文件夹地址'])
        self.setLayout(self.layout)

    def add_paths(self):
        row = 0
        for item in self.path_list:
            self.view_table.setItem(0, row, QTableWidgetItem(os.path.abspath(item)))
            row += 1

    def apply_paths(self):
        res = QMessageBox.question(self, '问题', '确认修改TkPy3 Path?', QMessageBox.Yes | QMessageBox.No,
                                   QMessageBox.Yes)
        if res == QMessageBox.Yes:
            add_config('TkPy3_path', self.path_list)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = PathWidget()
    widget.setWindowIcon(QIcon(os.path.join(BASE_DIR, "images", "icons", "python.png")))
    widget.setWindowTitle('Python Path 管理器')
    widget.show()
    sys.exit(app.exec_())
