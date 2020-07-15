import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
command = f"python \
{os.path.join(BASE_DIR, 'tkpy3_tools/i18n_tools', 'pygettext.py')} -o locale/tkpy3.pot __init__.py"
os.chdir(BASE_DIR)
# python E:\TkPy3\TkPy3\tkpy3_tools\i18n_tools\msgfmt.py -o tkpy3.mo tkpy3.po
os.system(command)
