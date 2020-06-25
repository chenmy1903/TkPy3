# -*- coding: UTF-8 -*-
# -------------------------------
# | TkPy3 tools compile pyd file|
# -------------------------------
# Chenmy1903 © 2020 All Rights Reserved
from TkPy3.tkpy3_tools.extension import TkPyExtensionType
import sys
import subprocess

__version__ = '0.0.0'

compile_file_text = """
import distutils
import os
from Cython.Build import cythonize
distutils.setup(
  ext_modules = cythonize(os.path.abspath({file_name})),
)
"""
command = f"{sys.executable} setup.py build_ext --inplace"
extension_config = TkPyExtensionType('编译Pyd文件', __version__)
