# -*- coding: UTF-8 -*-
from pip._internal.main import main as PipMain


class tkpy_pip:
    def install(self, *packages):
        return PipMain(['install', *packages])

    def uninstall(self, *packages):
        return PipMain(['uninstall', *packages, '-y'])

    def force_reinstall(self, *packages):
        return PipMain(['install', *packages, '--force-reinstall'])

    def upgrade(self, *packages):
        return PipMain(['install', '--upgrade', *packages])

    def exec_(self, *args):
        return PipMain(args)
