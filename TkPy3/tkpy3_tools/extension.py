import os
import types
import zipfile

from TkPy3.tkpy3_tools.errors import NoSetupError
from TkPy3.tkpy3_tools.tkpy_file import config_path as user_install_path


class TkPyExtensionType(dict):
    name: str
    version: str
    command: types.FunctionType

    def __init__(self, name: str, version: str = None, command: types.FunctionType = lambda: None, **kwargs):
        dict.__init__(self, name=name, version=version,
                      command=command, **kwargs)

    def __repr__(self):
        commands = [f'{key}={repr(value)}' for key, value in self.items()]
        return 'TkPyExtensionType({})'.format(", ".join(commands))

    def set_command(self, command: types.FunctionType):
        self['command'] = command

    def __getattribute__(self, name):
        try:
            return self[name]
        except KeyError:
            return dict.__getattribute__(self, name)

    def __setattr__(self, key, value):
        self[key] = value


if __name__ == "__main__":
    print(TkPyExtensionType(__name__))
