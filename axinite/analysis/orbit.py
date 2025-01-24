import axinite as ax
import axinite.analysis as axana
from numba import jit
import numpy as np

class Orbit:
    def __init__(self, central: ax.Body, satellite: ax.Body):
        self.central = central
        "The central body of the orbit."

        self.satellite = satellite
        "The satellite of the orbit."

        self.apogee, self.perigee = self._apogee_perigee()
        "The apogee/perigee of the orbit."

        self.eccentricity = self._eccentricity()
        "The eccentricity of the orbit."

        self.inclination = self._inclination()
        "The inclination of the orbit in radians."

        self.inclination_deg = np.degrees(self.inclination)
        "The inclination of the orbit in degrees."

        self.semi_major_axis = self._semi_major_axis()
        "The semi-major axis of the orbit."

        self.orbital_period = self._orbital_period()
        "The orbital period of the orbit in seconds."

        self.orbital_velocity = self._orbital_velocity()
        "The orbital velocity of the orbit in meters per second."

    def _apogee_perigee(self):
        relative = self.satellite._inner["r"] - self.central._inner["r"]
        absolute = np.linalg.norm(relative, axis=1)
        max_index = np.argmax(absolute)
        min_index = np.argmin(absolute)
        apogee = absolute[max_index]
        perigee = absolute[min_index]
        return (apogee, perigee)
    
    def _eccentricity(self):
        apogee_magnitude = np.linalg.norm(self.apogee)
        perigee_magnitude = np.linalg.norm(self.perigee)
        return (apogee_magnitude - perigee_magnitude) / (apogee_magnitude + perigee_magnitude)
    
    def _inclination(self):
        relative = self.satellite._inner["r"] - self.central._inner["r"]
        z = relative[:, 2]
        r = np.linalg.norm(relative, axis=1)
        return np.arccos(z / r)

    def _semi_major_axis(self):
        apogee_magnitude = np.linalg.norm(self.apogee)
        perigee_magnitude = np.linalg.norm(self.perigee)
        return (apogee_magnitude + perigee_magnitude) / 2
    
    def _orbital_period(self):
        total_mass = self.central.mass + self.satellite.mass
        return 2 * np.pi * np.sqrt(self.semi_major_axis**3 / (total_mass * ax.G))

    def _orbital_velocity(self):
        return 2 * np.pi * self.semi_major_axis / self._orbital_period()
    