from astropy.coordinates import CartesianRepresentation
from astropy.constants import G
import axinite as ax
import astropy.units as u
from numpy import float64

class Body:
    "A class that represents a body in the simulation."
    def __init__(self, name: str, mass: u.Quantity, position: CartesianRepresentation, velocity: CartesianRepresentation, radius: u.Quantity, color: str = "", light: bool = False, retain = None, radius_multiplier = 1):
        """Initializes a new Body object.

        Args:
            name (str): The body's name.
            mass (u.Quantity): The mass of the body in kilograms.
            position (CartesianRepresentation): The initial position of the body (in vector form).
            velocity (CartesianRepresentation): The initial velocity of the body (in vector form).
            radius (u.Quantity): The radius of the body in meters.
            color (str, optional): The color of the body. Defaults to "", telling the frontend to choose from a list.
            light (bool, optional): Whether the body should give of light. Defaults to False.
            retain (_type_, optional): How many points the body should retain on it's trail. Defaults to None, meaning "go with default".
            radius_multiplier (int, optional): A multiplier to be applied to the radius. Defaults to 1.
        """

        self.mass: u.Quantity = mass
        "The mass of the body in kilograms."

        self.r: dict[float64, CartesianRepresentation] = { float64(0): position}
        "The position of the body at each timestep."

        self.v: dict[float64, CartesianRepresentation] = { float64(0): velocity}
        "The velocity of the body at each timestep."

        self.name: str = name
        "The name of the body."

        self.radius: u.Quantity = radius * radius_multiplier
        "The radius of the body in meters."

        self.color: str = color
        "The color of the body."

        self.light: bool = light
        "Whether the body should give off light."

        self.retain: int = retain
        "How many points the body should retain on it's trail."

        self.radius_multiplier: int = radius_multiplier
        "A multiplier which was applied to the radius."