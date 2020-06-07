# -*- coding: UTF-8 -*-
import jedi
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *
import autopep8

from TkPy3.default_configs import get_configs, add_diff
from TkPy3.tkpy3_tools.text import TkPyTextEdit
import qdarkstyle
import sys


class BaseEditor(QWidget):
    def __init__(self, parent=None, read_only=False):
        QWidget.__init__(self, parent=parent)
        add_diff()
        self.edit_frame = QHBoxLayout()
        self.file_name = ""
        self.text = QTextBrowser(self) if read_only else TkPyTextEdit()
        self.text_cursor = self.text.textCursor()
        self.get_start()

    def get_start(self):
        self.text.setWordWrapMode(get_configs()['text_wrap'])
        self.text.setFont(QFont(get_configs()['font_name']))
        self.edit_frame.addWidget(self.text)
        self.text.setPlainText(get_configs()['init_text'])
        self.text.setTabStopWidth(get_configs()['tab_width'] * 10)
        self.setLayout(self.edit_frame)

    def open(self, file_name: str):
        with open(file_name, encoding=get_configs()['default_file_encoding']) as f:
            self.text.setPlainText(f.read())
        self.file_name = file_name
        self.setWindowTitle(file_name)

    def save_file(self, file_name: str):
        try:
            with open(file_name, 'w', encoding=get_configs()['default_file_encoding']) as f:
                f.write(self.text.toPlainText())
        except PermissionError:
            QMessageBox.critical(self, '错误', '无权利访问文件。', QMessageBox.Ok)
        else:
            self.file_name = file_name
        self.setWindowTitle(file_name)

    def autopep8_fix_code(self):
        text = autopep8.fix_code(self.text.toPlainText())
        self.text.setText(text)
        
    def run(self):
        QMessageBox.information(self, 'TkPy测试', '运行')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dark_stylesheet = qdarkstyle.load_stylesheet_pyqt5()
    app.setStyleSheet(dark_stylesheet)
    widget = BaseEditor()
    widget.setWindowTitle('TkPy3 Test')
    widget.show()
    sys.exit(app.exec_())
