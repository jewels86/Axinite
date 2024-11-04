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
        r_vector = other.position - self.position
        r = r_vector.norm()
        uv = r_vector / r
        g_magnitude = (G * self.mass * r**2).to(u.meter / u.second**2)
        g_vector = -g_magnitude * uv
        return CartesianRepresentation(g_vector.x, g_vector.y, g_vector.z)