# -*- coding: UTF-8 -*-
import os

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QStyleFactory

from TkPy3.locale_dirs import pixmaps
from TkPy3.default_configs import get_configs


def set_icon_to_tkpy3(app: QApplication):
    return app.setWindowIcon(QIcon(pixmaps['tkpy3']))


def set_style(app: QApplication):
    return app.setStyle(QStyleFactory.create(get_configs()['window_style']))


def setup(app: QApplication):
    set_style(app)
    set_icon_to_tkpy3(app)
    return app


def check_system():
    if os.name != 'nt':
        raise SystemError('TkPy3 only run on Windows.')


tkpy3_setup = setup
