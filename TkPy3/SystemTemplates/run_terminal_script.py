import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

command = f'start cmd /Q /K "{sys.executable} -u {os.path.join(BASE_DIR, "print_envs.py")}"'

if __name__ == "__main__":
    os.system(command)
