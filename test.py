from astropy.coordinates import CartesianRepresentation
import astropy.units as u
import axinite as ax
import numpy as np
import math

earth = ax.Body(
    5.972e24 * u.kg,
    CartesianRepresentation([0, 0, 0] * u.m),
    CartesianRepresentation([0, 0, 0] * u.m/u.s)
)
moon = ax.Body(
    7.342e22 * u.kg,
    CartesianRepresentation([3.844e8, 0, 0] * u.m),
    CartesianRepresentation([1.095e3, 0, 0] * u.m/u.s)
)

