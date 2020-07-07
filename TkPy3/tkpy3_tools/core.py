import ctypes
import sys
import os


def is_venv():
    for activate_name in ['activate', 'activate.bat', 'Activate.ps1']:
        if activate_name in os.listdir(os.path.dirname(sys.executable)):
            return True
    return False


def windows_set_taskbar_icon():
    if os.name == 'nt':
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('TkPy3')


def gen_style(style: dict):
    for key, value in style.items():
        style[key] = value.replace(':', ' ').split(' ')[-1]
    return style
