# -*- coding: UTF-8 -*-

from PyQt5.QtGui import QColor, QIcon, QIntValidator
from PyQt5.QtWidgets import QWidget, QDialog, QLineEdit, QDialogButtonBox, QFormLayout, QApplication, QMessageBox

import typing


def load_icon(path: str, widget: QWidget):
    widget.setWindowIcon(QIcon(path))


class RGB:
    R, G, B = [0 for i in range(3)]

    def __init__(self, r: int, g: int, b: int):
        rgb = r, g, b
        self.R, self.G, self.B = r, g, b
        if (r, g, b) > (255, 255, 255):
            raise ValueError(f'Is not a rgb color. {(r, g, b)}')
        strs = '#'
        for i in rgb:
            num = i
            strs += str(hex(num))[-2:].replace('x', '0').upper()
        self.__rgb_str = strs

    def __repr__(self):
        return self.__rgb_str

    def __str__(self):
        return str(self.__rgb_str)

    def to_pyqt_color(self):
        return QColor(self.__rgb_str)

    def __bool__(self):
        return True

    def __getitem__(self, color: str):
        color = color.upper()
        if color not in ['R', 'G', 'B']:
            raise ValueError('Is not a color code.')
        return getattr(self, color)
