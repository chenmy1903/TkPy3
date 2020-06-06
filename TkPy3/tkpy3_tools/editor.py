# -*- coding: UTF-8 -*-
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *
import autopep8
from TkPy3.default_configs import get_configs, add_diff
import qdarkstyle
import sys


class BaseEditor(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        add_diff()
        self.edit_frame = QVBoxLayout()
        self.text = QTextEdit(self)
        self.dark_stylesheet = qdarkstyle.load_stylesheet_pyqt5()
        self.get_start()

    def get_start(self):
        self.text.setWordWrapMode(get_configs()['text_wrap'])
        self.text.setFont(QFont(get_configs()['font_name']))
        self.edit_frame.addWidget(self.text)
        self.setStyleSheet(self.dark_stylesheet)
        self.setLayout(self.edit_frame)

    def autopep8_fix_code(self):
        text = autopep8.fix_code(self.text.toPlainText())
        self.text.setText(text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = BaseEditor()
    widget.setWindowTitle('TkPy3 Test')
    widget.show()
    sys.exit(app.exec_())
