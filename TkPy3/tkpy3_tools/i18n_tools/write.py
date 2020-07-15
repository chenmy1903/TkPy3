from TkPy3.tkpy3_tools.i18n_tools.msgfmt import make
from TkPy3.tkpy3_tools.i18n_tools.pygettext import pot_header


def write_translate(translate: dict, file_name: str):
    with open(file_name, 'w', encoding='UTF-8') as f:
        f.write(pot_header)
        for key, value in translate.items():
            f.write('msgid ' + repr(key))
            f.write('msgstr ' + repr(value))
    make(file_name)
