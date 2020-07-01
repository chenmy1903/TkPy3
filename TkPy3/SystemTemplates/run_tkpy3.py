# -*- coding: UTF-8 -*-
import sys
import os
import runpy

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)
runpy.run_module('TkPy3')

