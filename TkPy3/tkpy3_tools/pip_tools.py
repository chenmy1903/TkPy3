# -*- coding: UTF-8 -*-
import sys
import os


class tkpy_pip(object):
    def __init__(self):
        object.__init__(self)

    def install(self, *packages):
        return os.system(f'{sys.executable} -m pip install {" ".join(packages)} --timeout 1000')

    def uninstall(self, *packages):
        return os.system(f'{sys.executable} -m pip uninstall {" ".join(packages)} -y')

    def force_reinstall(self, *packages):
        return os.system(f'{sys.executable} -m pip install {" ".join(packages)} --force-reinstall --timeout 1000')

    def upgrade(self, *packages):
        return os.system(f'{sys.executable} -m pip install {" ".join(packages)} --upgrade --timeout 1000')

    def __call__(self, *args):
        return os.system(f'{sys.executable} -m pip {" ".join(args)}')
