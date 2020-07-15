# -*- coding: UTF- -*-
import posixpath
import sys
import requests
from bs4 import BeautifulSoup
import os
from typing import Tuple

from pip._internal.commands.show import search_packages_info
from pip._internal.utils.misc import get_installed_distributions


class PyPiError(Exception):
    """Error for tkpy3.tkpy3_tools.pip_tools"""


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

    def get_all_packages(self):
        installed_packages = get_installed_distributions()
        for package in installed_packages:
            yield package.project_name, package.version, package.location

    def get_package_info(self, package_name: str):
        distributions = search_packages_info([package_name])
        messages = {}
        for dist in distributions:
            messages['name'] = dist.get('name', '')
            messages['version'] = dist.get('version', '')
            messages['summary'] = dist.get('summary', '')
            messages['home-page'] = dist.get('home-page', '')
            messages['anthor'] = dist.get('author', '')
            messages['location'] = dist.get('location', '')
            messages['requires'] = dist.get('requires', [])
            messages['requires_by'] = dist.get('required_by', [])
        return messages


if __name__ == "__main__":
    for name, version, location in tkpy_pip().get_all_packages():
        print(tkpy_pip().get_package_info(name))
