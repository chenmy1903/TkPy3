import gettext
import os

from TkPy3.locale_dirs import BASE_DIR

_ = gettext.Catalog('tkpy3', os.path.join(BASE_DIR, 'locale'), ['zh-CN']).gettext

