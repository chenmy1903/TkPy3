# -*- coding: UTF-8 -*-
import PyQt5
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
images_icon_dir = os.path.join(BASE_DIR, 'images', 'icons')
static_dir = os.path.join(BASE_DIR, 'tkpy_static')
PYQT5_PATH = os.path.dirname(PyQt5.__file__)
pixmaps = {
    'run': os.path.join(images_icon_dir, 'editor_icons', 'run.png'),
    'shell': os.path.join(images_icon_dir, 'shell_icons', 'pyshell.ico'),
    'new_file': os.path.join(images_icon_dir, 'editor_icons', 'filenew.png'),
    'open_file': os.path.join(images_icon_dir, 'editor_icons', 'fileopen.png'),
    'save_file': os.path.join(images_icon_dir, 'editor_icons', "filesave.png"),
    'saveas_file': os.path.join(images_icon_dir, 'editor_icons', "filesaveas.png"),
    'exit': os.path.join(images_icon_dir, 'editor_icons', 'fileclose.png'),
    'restart': os.path.join(images_icon_dir, 'editor_icons', 'restart_window.jpg'),
    'close_all': os.path.join(images_icon_dir, 'editor_icons', "filecloseall.png"),
    'config': os.path.join(images_icon_dir, 'config_icons', 'advanced.png'),
    'python_file': os.path.join(images_icon_dir, 'file_icons', 'py.ico'),
    'search': os.path.join(images_icon_dir, 'editor_icons', 'search.png'),
    'python_icon': os.path.join(images_icon_dir, 'editor_icons', 'python_icon.ico'),
}
