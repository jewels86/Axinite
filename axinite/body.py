from astropy.coordinates import CartesianRepresentation
from astropy.constants import G
import astropy.units as u
from math import pi

class Body:
    def __init__(self, name: str, mass: u.Quantity, position: CartesianRepresentation, velocity: CartesianRepresentation, avg_radius: u.Quantity, volume: u.Quantity = -1):
        """
        Initialize a new celestial body.
        
        Parameters:
        - `name` (`str`): The name of the celestial body.
        - `mass` (`Quantity`): The mass of the celestial body.
        - `position` (`CartesianRepresentation`): The position of the celestial body in Cartesian coordinates.
        - `velocity` (`CartesianRepresentation`): The velocity of the celestial body in Cartesian coordinates.
        """
        
        self.name = name
        self.mass = mass
        self.position = position
        self.velocity = velocity
        self.volume = volume if volume != -1 else (4/3) * pi * avg_radius**3
        self.avg_radius = avg_radius
        
        self.escape_velocity = (2 * G * self.mass.to(u.kilogram) / self.avg_radius.to(u.meter))
        self.density = self.mass / self.volume
        
    def gravitational_force(self, other: 'Body'):
        r_dist = other.position - self.position # distance vector between A and B
        r = r_dist.norm() # magnitude of rAB
        uv = r_dist / r
        
        return -((G * self.mass) / r**2) * uv