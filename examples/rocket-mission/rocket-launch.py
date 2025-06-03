import axinite as ax
import axinite.tools as axtools
import axinite.analysis as axana
import axinite.utils as axutils
from numba import njit
import numpy as np
import logging, sys, os

path = "system-configuration.tmpl.ax"
launch_planet = "Earth"
destination_planet = "Mars"

logger = logging.getLogger('rocket-log')

_sc_args = None
try:
    with open(path) as f:
        logger.info(f"System configuration file found at path {path}, loading into '_sc_args'")
    _sc_args = axtools.read(path)
except:
    logger.warning("No system-configuration file found- did you run the pre-launch script?")
    sys.exit(-1)
sc_args: axtools.AxiniteArgs = _sc_args
logger.info(f"Checking for launch planet '{launch_planet}'")
