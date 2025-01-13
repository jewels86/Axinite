import axinite.tools as axtools
import numpy as np

class AxiniteArgs:
    """
    A class to store simulation parameters for the Axinite celestial mechanics engine.

    Attributes:
        name (str): The name of the simulation.
        delta (np.float64): The frequency at which the simulation should be computed in seconds.
        limit (np.float64): The length of the simulation in seconds.
        action (function): A function to be called at each timestep.
        t (np.float64): The current timestep.
        bodies (list[axtools.Body]): A list of Body objects to be simulated.
        radius_multiplier (float): A float to multiply all radii by.
        rate (int): The number of frames per second to render for the live and run functions.
        retain (int): The number of points to retain on each body's trail.
        modifier (function): A function called to modify the forces on the bodies.
        frontend_args (dict[str, dict[str, str|float|int|bool|list|dict]]): A dictionary of frontend-specific arguments.
        backend (function): The backend (integration method) to use.
        action_frequency (int): The frequency at which the action function should be called.
    """
    
    def __init__(self):
        """Initializes an AxiniteArgs object."""

        self.name: str = None
        "The name of the simulation."

        self.delta: np.float64 = None
        "The frequency at which the simulation should be computed in seconds."

        self.limit: np.float64 = None
        "The length of the simulation in seconds."

        self.action: function = None
        "A function to be called at each timestep."

        self.t: np.float64 = None
        "The current timestep."

        self.bodies: list[axtools.Body] = []
        "A list of Body objects to be simulated."

        self.radius_multiplier: float = None
        "A float to multiply all radii by."

        self.rate: int = None
        "The number frames per second to render for the live and run functions."

        self.retain: int = None
        "The number of points to retain on each body's trail."

        self.modifier: function = None
        "A function called to modify the forces on the bodies."

        self.frontend_args: dict[str, dict[str, str|float|int|bool|list|dict]] = {}
        "A dictionary of frontend-specific arguments."

        self.backend: function = None
        "The backend (integration method) to use."

        self.action_frequency: int = None
        "The frequency at which the action function should be called."

    def unpack(self) -> tuple[np.float64, np.float64, 'function', '*tuple[axtools.Body, ...]']:
        """
        Unpacks the AxiniteArgs object into a tuple that can be passed to `axinite`'s load function.

        Returns:
            tuple: A tuple containing delta, limit, action, and bodies.
        """
        return self.delta, self.limit, self.backend, *self.bodies