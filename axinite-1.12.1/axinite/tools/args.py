import axinite.tools as axtools
import numpy as np

class AxiniteArgs:
    "A class to store simulation parameters."
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
        """Unpacks the AxiniteArgs object into a tuple that can be passed in `axinite`'s load function.

        Returns:
            *tuple[u.Quantity, u.Quantity, *tuple[axtools.Body, ...]]: An unpackable tuple of the core simulation parameters.
        """
        return self.delta, self.limit, self.backend, *self.bodies