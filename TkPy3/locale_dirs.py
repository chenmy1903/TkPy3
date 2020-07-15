# -*- coding: UTF-8 -*-
import PyQt5
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
images_icon_dir = os.path.join(BASE_DIR, 'images', 'icons')
static_dir = os.path.join(BASE_DIR, 'tkpy_static')
PYQT5_PATH = os.path.dirname(PyQt5.__file__)
pixmaps = {
    'run': os.path.join(images_icon_dir, 'oxygen', 'runScript.png'),
    'shell': os.path.join(images_icon_dir, 'shell.svg'),
    'terminal': os.path.join(images_icon_dir, 'terminal.svg'),
    'new_file': os.path.join(images_icon_dir, 'new.svg'),
    'open_file': os.path.join(images_icon_dir, 'open.svg'),
    'save_file': os.path.join(images_icon_dir, 'fileSave.svg'),
    'saveas_file': os.path.join(images_icon_dir, 'fileSaveAs.svg'),
    'save_all_file': os.path.join(images_icon_dir, 'fileSaveAll.svg'),
    'exit': os.path.join(images_icon_dir, 'exit.svg'),
    'close': os.path.join(images_icon_dir, 'close.svg'),
    'restart': os.path.join(images_icon_dir, 'oxygen', 'restart.png'),
    'close_all': os.path.join(images_icon_dir, 'oxygen', 'projectClose.png'),
    'config': os.path.join(images_icon_dir, 'ircConfigure.svg'),
    'python_file': os.path.join(images_icon_dir, 'filePython.svg'),
    'search': os.path.join(images_icon_dir, 'preferences-search.svg'),
    'python_icon': os.path.join(images_icon_dir, 'preferences-python.svg'),
    'tkpy3': os.path.join(images_icon_dir, 'TkPy.bmp'),
    'copy': os.path.join(images_icon_dir, 'editCopy.svg'),
    'paste': os.path.join(images_icon_dir, 'editPaste.svg'),
    'cut': os.path.join(images_icon_dir, 'editCut.svg'),
    'undo': os.path.join(images_icon_dir, 'editUndo.svg'),
    'redo': os.path.join(images_icon_dir, 'editRedo.svg'),
    'help_about': os.path.join(images_icon_dir, 'helpAbout.svg'),
    'about_qt': os.path.join(images_icon_dir, 'helpAboutQt.svg'),
    'ui_previewer': os.path.join(images_icon_dir, 'uiPreviewer.svg'),
    'search': os.path.join(images_icon_dir, 'preferences-search.svg')
}
