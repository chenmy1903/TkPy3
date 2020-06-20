# -*- coding: UTF-8 -*-
import platform
import os
from TkPy3.tkpy3_tools.tkpy_file import tkpy_file, read_tkpy_file
from TkPy3.locale_dirs import BASE_DIR

events = {}

configs = {
    'init_title': f'TkPy3 (Python {platform.python_version()})',
    'init_text': '# -*- coding: UTF-8 -*-\n',
    'init_icon_path': os.path.join(BASE_DIR, 'images', 'icons', 'TkPy.bmp'),
    'text_wrap': False,
    'font_name': '黑体',
    'TkPy3_path': ['.'],
    'new_file_title': 'Untitled',
    'default_file_encoding': 'UTF-8',
    'auto_save': False,
    'highlight_style': 'tango',
    'tab_width': 4,
    'line_background_color': '#1f0000ff',
    'eol_mode': 'Unix',
    'indent_with_tabs': False,
    'cursor_color': '#ff0000ff',
    'permanent_activation_codes': ['ANBC-NBDG-MPTY-TUYD'],
    'activate_codes': [],
    'is_activate': False,
    'end_activate_day': False,
    'events': events,
    'window_style': 'Windows',  # ['windowsvista', 'Windows', 'Fusion']
}


def reset_configs():
    old = get_configs()
    end_activate_day = old['end_activate_day']
    is_activate = old['is_activate']
    activate_codes = old['activate_codes']
    permanent_activation_codes = old['permanent_activation_codes']
    f = tkpy_file('config', configs)
    f.reset()
    f.add('end_activate_day', end_activate_day)
    f.add('is_activate', is_activate)
    f.add('permanent_activation_codes', permanent_activation_codes)
    f.add('activate_codes', activate_codes)
    return f


def get_configs(file_name='config'):
    add_diff()
    return read_tkpy_file(file_name)


def add_diff():
    f = tkpy_file('config', configs)
    f_text = f.read()
    for key, value in configs.items():
        if key not in f_text:
            f.add(key, value)


def add_config(key, value):
    f = tkpy_file('config', configs)
    f.add(key, value)


if __name__ == '__main__':
    new_config: dict = reset_configs().read()
    for key, value in new_config.items():
        key = key if not isinstance(key, str) else repr(key)
        value = value if not isinstance(value, str) else repr(value)
        print(key, value, sep=': ')
