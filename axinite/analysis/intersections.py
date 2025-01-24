import axinite as ax
import numpy as np
from numba import jit

@jit
def _intersection(a: np.ndarray, b: np.ndarray)