import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
python = sys.executable
pip = sys.executable + ' -m pip'

print('*' * 80)
print('\t\tTkPy3 Terminal')
print(' ' * 10 + 'Some terminal command:' + ' ' * 20)
print(' -Python == {}'.format(python))
print(' -Pip    == {}'.format(pip))
print('*' * 80)
