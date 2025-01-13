import numpy as np
import axinite as ax

class Body:
    """
    A class that represents a body in the simulation.

    Attributes:
        name (str): The body's name.
        mass (np.float64): The mass of the body in kilograms.
        position (np.ndarray): The initial position of the body (in vector form).
        velocity (np.ndarray): The initial velocity of the body (in vector form).
        radius (np.float64): The radius of the body in meters.
        color (str): The color of the body.
        light (bool): Whether the body should give off light.
        retain (int): How many points the body should retain on its trail.
        radius_multiplier (int): A multiplier to be applied to the radius.
    """

    def __init__(self, name: str, mass: np.float64, limit: np.float64, delta: np.float64, position: np.ndarray = None, velocity: np.ndarray = None):
        """
        Initializes a new Body object.

        Args:
            name (str): The body's name.
            mass (np.float64): The mass of the body in kilograms.
            limit (np.float64): The length of the simulation in seconds.
            delta (np.float64): The frequency at which the simulation should be computed in seconds.
            position (np.ndarray, optional): The initial position of the body (in vector form). Defaults to None.
            velocity (np.ndarray, optional): The initial velocity of the body (in vector form). Defaults to None.
        """
        
        self.mass = mass
        "The mass of the object in kilograms."

        self.name = name
        "The name of the object."

        self._inner = ax._body(limit, delta, name, mass)

        if position is not None: self._inner["r"][0] = position
        if velocity is not None: self._inner["v"][0] = velocity

        self._inner["n"] = name
        self._inner["m"] = mass

    def r(self, t: np.float64) -> np.ndarray:
        """Returns the position of the object at a specific time.

        Args:
            t (np.float64): The time to get the position at.

        Returns:
            np.ndarray: The position of the object at the time.
        """
        return self._inner["r"][int(t)]

    def v(self, t: np.float64) -> np.ndarray:
        """Returns the velocity of the object at a specific time.

        Args:
            t (np.float64): The time to get the velocity at.

        Returns:
            np.ndarray: The velocity of the object at the time.
        """
        return self._inner["v"][int(t)]