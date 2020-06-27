# -*- coding: UTF-8 -*-
from PyQt5 import QtGui
from PyQt5.QtGui import QFont
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import *
import autopep8

from TkPy3.default_configs import get_configs, add_diff
from TkPy3.tkpy3_tools.find import TkPyFindWidget
from TkPy3.tkpy3_tools.start import tkpy3_setup
from TkPy3.tkpy3_tools.text import TkPyTextEdit, assert_text
import sys


class EditSubWindow(QMdiSubWindow):
    save = True
    number = 0
    close_remove = pyqtSignal()

    def setSave(self, b: bool):
        self.save = b

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        res = QMessageBox.No
        if not self.save:
            res = QMessageBox.question(self, 'TkPy3 - SubWindow', f'文件{self.windowTitle()}未保存，是否保存之后退出子窗口?',
                                       QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
                                       QMessageBox.Cancel)
        if res == QMessageBox.Yes:
            file_name, ok = QFileDialog.getSaveFileName(
                self, '保存文件', '', 'Python 源文件 (*.py *.pyw)')
            if ok:
                self.widget().save_file(file_name)
            event.accept()
            self.close_remove.emit()
        elif res == QMessageBox.No:
            event.accept()
            self.close_remove.emit()
        else:
            event.ignore()

    def setNumber(self, number: int):
        self.number = number


class BaseEditor(QWidget):
    not_save = pyqtSignal()
    save = pyqtSignal()

    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        add_diff()
        self.edit_frame = QVBoxLayout()
        self.file_name = ""
        self.text = TkPyTextEdit()
        self.get_start()

    def get_start(self):
        self.text.setFont(QFont(get_configs()['font_name']))
        self.edit_frame.addWidget(self.text)
        self.text.setText(get_configs()['init_text'])
        self.setLayout(self.edit_frame)
        self.text.key_pressed.connect(self.assert_text)

    def open(self, file_name: str):
        with open(file_name, encoding=get_configs()['default_file_encoding']) as f:
            self.text.setText(f.read())
        self.file_name = file_name
        self.setWindowTitle(self.file_name)
        self.text.setMarginWidth(
            0, len(str(len(self.text.text().split('\n')))) * 20)

    def save_file(self, file_name: str):
        try:
            with open(file_name, 'w', encoding=get_configs()['default_file_encoding']) as f:
                f.write(self.text.text())
        except PermissionError:
            QMessageBox.critical(self, '错误', '无权利访问文件。', QMessageBox.Ok)
        else:
            self.file_name = file_name
            self.setWindowTitle(self.file_name)
            self.assert_text()

    def autopep8_fix_code(self):
        text = autopep8.fix_code(self.text.text())
        self.text.setText(text)
        self.assert_text()

    def run(self):
        QMessageBox.information(self, 'TkPy测试', '运行')

    def assert_text(self):
        if self.file_name:
            with open(self.file_name, encoding=get_configs()['default_file_encoding']) as f:
                if assert_text(self.text.text(), f.read()):
                    self.not_save.emit()
                else:
                    self.save.emit()
        else:
            if assert_text(self.text.text().replace('\r', ''), get_configs()['init_text']):
                self.not_save.emit()
            else:
                self.save.emit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = BaseEditor()
    tkpy3_setup(app)
    widget.setWindowTitle('TkPy3 Test')
    widget.show()
    sys.exit(app.exec_())
