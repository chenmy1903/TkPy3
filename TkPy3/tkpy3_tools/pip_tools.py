# -*- coding: UTF-8 -*-
from pip._internal.main import main as PipMain


class tkpy_pip(object):
    def __init__(self):
        object.__init__(self)

    def install(self, *packages):
        return PipMain(['install', *packages, '-i https://pypi.doubanio.com/simple'])

    def uninstall(self, *packages):
        return PipMain(['uninstall', *packages, '-y'])

    def force_reinstall(self, *packages):
        return PipMain(['install', *packages, '--force-reinstall', '-i https://pypi.doubanio.com/simple'])

    def upgrade(self, *packages):
        return PipMain(['install', '--upgrade', *packages, '-i https://pypi.doubanio.com/simple'])

    def __call__(self, *args):
        return PipMain(args)
