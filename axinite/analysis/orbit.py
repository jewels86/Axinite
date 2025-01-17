import axinite as ax
import axinite.analysis as axana
import numpy as np

class Orbit:
    def __init__(self, central: ax.Body, satellite: ax.Body):
        self.central = central
        self.satellite = satellite
        self.n_timesteps = central._inner["r"].shape[0]
        self.apogee, self.perigee = self._apogee_perigee()
        self.eccentricity = self._eccentricity()
        self.inclination = self._inclination()
        self.inclination_deg = np.degrees(self.inclination)
        self.semi_major_axis = self._semi_major_axis()
        self.orbital_period = self._orbital_period()
        self.orbital_velocity = self._orbital_velocity()

    def _apogee_perigee(self):
        relative = self.satellite._inner["r"] - self.central._inner["r"]
        absolute = np.abs(relative)
        apogee = np.max(absolute)
        perigee = np.min(absolute)
        return (apogee, perigee)
    
    def _eccentricity(self):
        return (self.apogee - self.perigee) / (self.apogee + self.perigee)
    
    def _inclination(self):
        relative = self.satellite._inner["r"] - self.central._inner["r"]
        z = relative[:, 2]
        r = np.linalg.norm(relative, axis=1)
        return np.arccos(z / r)

    def _semi_major_axis(self):
        return (self.apogee + self.perigee) / 2
    
    def _orbital_period(self):
        return 2 * np.pi * np.sqrt(self.semi_major_axis**3 / (self.central.mass * ax.G))

    def _orbital_velocity(self):
        return 2 * np.pi * self.semi_major_axis / self._orbital_period()