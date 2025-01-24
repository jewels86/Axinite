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
        if position is not None:
            position = np.array(position, dtype=np.float64)
        if velocity is not None:
            velocity = np.array(velocity, dtype=np.float64)
        mass = np.float64(mass)
        limit = np.float64(limit)
        delta = np.float64(delta)
        
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

    @property
    def rs(self) -> np.ndarray: return self._inner["r"]
    @property
    def vs(self) -> np.ndarray: return self._inner["v"]