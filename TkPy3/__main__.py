from . import main
from .locale_dirs import BASE_DIR

import sys

if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)
if __name__ == "__main__":
    main()
