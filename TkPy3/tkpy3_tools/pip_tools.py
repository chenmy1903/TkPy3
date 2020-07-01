# -*- coding: UTF- -*-
import posixpath
import sys
import requests
from bs4 import BeautifulSoup
import os
from typing import Tuple

from pip._internal.utils.misc import get_installed_distributions


class PyPiError(Exception):
    """Error for tkpy3.tkpy3_tools.pip_tools"""


class PackageReport:
    def __init__(self, package_name: str):
        pass


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

    def get_pypi_packages(self, report="https://pypi.doubanio.com/"):
        user_agent = (
            'Mozilla/5.0 '
            '(Windows NT 6.1; WOW64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE')
        r = requests.get(posixpath.join(report, 'simple'), {'User-Agent': user_agent})
        soup = BeautifulSoup(r.text, 'html.parser')
        all_package = []
        for link in soup.find_all('a'):
            all_package.append(link.get('href').replace('/simple/', '/').replace('/', ''))
        return tuple(all_package)

    def __call__(self, *args: Tuple[str]):
        return os.system(f'{sys.executable} -m pip {" ".join(args)}')

if __name__ == "__main__":
    for package in tkpy_pip().get_all_packages():
        print(package)
