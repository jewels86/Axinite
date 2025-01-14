"""
The `axtools` module provides a set of tools and utilities for working with the Axinite celestial mechanics engine.

This module includes classes and functions for handling simulation parameters, body objects, data loading and saving,
visualization frontends, and various utility functions.

Classes:
    AxiniteArgs: A class to store simulation parameters.
    Body: A class that represents a body in the simulation.

Functions:
    interpret_time(string: str) -> np.float64: Interprets a string as a time in seconds.
    interpret_mass(string: str) -> np.float64: Interprets a string as a mass in kilograms.
    interpret_distance(string: str) -> np.float64: Interprets a string as a distance in meters.
    data_to_body(data: dict[str, any], limit, delta) -> Body: Converts a dict to a Body object.
    string_to_color(color_name: str, frontend: Literal['vpython', 'mpl', 'plotly']) -> vp.color | str: Converts a string to a color object for a given frontend.
    create_sphere(pos: np.ndarray, radius: np.float64, n=20) -> tuple[np.ndarray, np.ndarray, np.ndarray]: Generates the vertices of a sphere.
    max_axis_length(*bodies: Body, radius_multiplier: int = 1) -> np.float64: Finds the maximum axis length of a set of bodies.
    min_axis_length(*bodies: Body, radius_multiplier: int = 1) -> np.float64: Finds the minimum axis length of a set of bodies.
    from_body(body: ax.Body) -> Body: Converts an ax.Body object to an axtools.Body object.
    load(args: AxiniteArgs, path: str = "", dont_change_args: bool = False, verbose: bool = False) -> list[Body]: Preloads a simulation.
    read(path: str) -> AxiniteArgs: Reads a simulation from a file.
    show(_args: AxiniteArgs, frontend: 'function') -> None: Statically displays the bodies in the simulation.
    live(args: AxiniteArgs, frontend: 'function') -> None: Watches a preloaded simulation live.
    run(_args: AxiniteArgs, frontend: 'function', backend = ax.verlet_nojit_backend) -> tuple[Body, ...]: Loads and displays a simulation simultaneously.
    vpython_frontend(args: AxiniteArgs, mode: str, **kwargs): Initializes the VPython frontend for visualizing the simulation.
    plotly_frontend(args: AxiniteArgs, mode: str, theme="plotly_dark", use_min=True): Initializes the Plotly frontend for visualizing the simulation.
    save(args: AxiniteArgs, path: str): Saves the simulation data to a file.
    combine(meta: dict, file: dict, indent=4) -> str: Combines a .meta.ax file and a .ax/.tmpl.ax file into a JSON string.
"""

from axinite.tools.args import AxiniteArgs
from axinite.tools.body import Body
from axinite.tools.functions import data_to_body, string_to_color, create_sphere, max_axis_length, min_axis_length, \
    from_body, sphere_has
from axinite.tools.load import load
from axinite.tools.read import read
from axinite.tools.show import show
from axinite.tools.live import live
from axinite.tools.run import run
from axinite.tools.frontends.vpython import vpython_frontend
from axinite.tools.frontends.plotly import plotly_frontend
from axinite.tools.save import save
from axinite.tools.combine import combine