# -*- coding: UTF- -*-
import sys
import os
from typing import Tuple

from pip._internal.utils.misc import get_installed_distributions


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

    def get_all_packages(self) -> Tuple[str]:

        installed_packages = get_installed_distributions()
        for package in installed_packages:
            yield package.project_name, package.version, package.location

    def __call__(self, *args: Tuple[str]):
        return os.system(f'{sys.executable} -m pip {" ".join(args)}')


if __name__ == "__main__":
    for i in tkpy_pip().get_all_packages():
        print(i)
