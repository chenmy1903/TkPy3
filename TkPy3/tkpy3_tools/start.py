# -*- coding: UTF-8 -*-
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QStyleFactory

from TkPy3.default_configs import get_configs


def set_icon_to_tkpy3(app: QApplication):
    return app.setWindowIcon(QIcon(get_configs()['init_icon_path']))


def set_style(app: QApplication):
    return app.setStyle(QStyleFactory.create(get_configs()['window_style']))


def setup(app: QApplication) -> "QApplication":
    set_style(app)
    set_icon_to_tkpy3(app)
    return app


tkpy3_setup = setup
