import sys
import sysconfig
from loguru import logger

from utils.time_helper import time_taken


@time_taken
def check_gil():
    if sysconfig.get_config_var("Py_GIL_DISABLED"):
        logger.warning(f"GIL is enabled: {sys._is_gil_enabled()}")
    else:
        logger.warning(f"GIL is enabled: {True}")
