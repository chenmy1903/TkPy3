# -*- coding: UTF-8 -*-
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import *
import autopep8
from TkPy3.default_configs import get_configs, add_diff
from TkPy3.tkpy3_tools.text import PygmentsHighlighter
import qdarkstyle
import sys


class BaseEditor(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        add_diff()
        self.edit_frame = QHBoxLayout()
        self.text = QTextEdit(self)
        PygmentsHighlighter(self.text).set_style(get_configs()['highlight_style'])
        self.get_start()

    def get_start(self):
        self.text.setWordWrapMode(get_configs()['text_wrap'])
        self.text.setFont(QFont(get_configs()['font_name']))
        self.edit_frame.addWidget(self.text)
        self.text.setPlainText(get_configs()['init_text'])

        self.setLayout(self.edit_frame)

    def open(self, file_name: str):
        with open(file_name, encoding=get_configs()['default_file_encoding']) as f:
            self.text.setPlainText(f.read())

    def autopep8_fix_code(self):
        text = autopep8.fix_code(self.text.toPlainText())
        self.text.setText(text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dark_stylesheet = qdarkstyle.load_stylesheet_pyqt5()
    app.setStyleSheet(dark_stylesheet)
    widget = BaseEditor()
    widget.setWindowTitle('TkPy3 Test')
    widget.show()
    sys.exit(app.exec_())
