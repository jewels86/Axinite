import numpy as np
import axinite as ax
from numba import njit
import ast, operator

G = 6.67430e-11

def body_dtype(limit: np.float64, delta: np.float64) -> np.dtype:
    """
    Returns the data type for a body.

    Args:
        limit (np.float64): The length of the simulation in seconds.
        delta (np.float64): The frequency at which the simulation should be computed in seconds.

    Returns:
        np.dtype: The data type for a body.
    """
    return np.dtype([
        ("n", "U20"),
        ("m", np.float64),
        ("r", np.float64, (int(limit/delta), 3)),
        ("v", np.float64, (int(limit/delta), 3))
    ])

def _body(limit: np.float64, delta: np.float64, name: str, mass: np.float64) -> np.ndarray: 
    """
    Creates a new body.

    Args:
        limit (np.float64): The length of the simulation in seconds.
        delta (np.float64): The frequency at which the simulation should be computed in seconds.
        name (str): The name of the body.
        mass (np.float64): The mass of the body in kilograms.

    Returns:
        np.ndarray: The new body.
    """
    return np.array((name, mass, np.zeros((int(limit/delta), 3)), np.zeros((int(limit/delta), 3))), dtype=ax.body_dtype(limit, delta))

def get_inner_bodies(bodies: list[ax.Body]) -> np.ndarray:
    """
    Returns the inner representations of a list of bodies.

    Args:
        bodies (list[ax.Body]): A list of Body objects.

    Returns:
        np.ndarray: The inner representation of the bodies.
    """
    _bodies = ()
    for body in bodies: _bodies += (body._inner,)
    return np.array(_bodies)

def create_outer_bodies(bodies: np.ndarray, limit: np.float64, delta: np.float64) -> list[ax.Body]:
    """
    Creates outer body representations from inner bodies.

    Args:
        bodies (np.ndarray): An array of inner body representations.
        limit (np.float64): The length of the simulation in seconds.
        delta (np.float64): The frequency at which the simulation should be computed in seconds.

    Returns:
        list[ax.Body]: A list of Body objects.
    """
    _bodies = []
    for body in bodies:
        _body = ax.Body(str(body["n"]), body["m"], limit, delta)
        _body._inner = body
        _bodies.append(_body)
    return _bodies

@njit 
def vector_magnitude_jit(vec: np.ndarray) -> np.float64:
    """
    Calculates the magnitude of a vector.

    Args:
        vec (np.ndarray): The vector to calculate the magnitude of.

    Returns:
        np.float64: The magnitude of the vector.
    """
    return np.sqrt(np.sum(vec**2))

@njit
def unit_vector_jit(vec: np.ndarray) -> np.ndarray:
    """Calculates the unit vector of a vector.

    Args:
        vec (np.ndarray): The vector to calculate the unit vector of.

    Returns:
        np.ndarray: The unit vector of the vector.
    """
    mag = vector_magnitude_jit(vec)
    return vec / mag if mag > 0 else vec

@njit
def gravitational_force_jit(m1: np.float64, m2: np.float64, r: np.ndarray, epsilon: np.float64 = 1e-10) -> np.ndarray:
    """Calculates the gravitational force between two bodies.

    Args:
        m1 (u.Quantity): The mass of the first body.
        m2 (u.Quantity): The mass of the second body.
        r (np.ndarray): The vector between the two bodies.
        epsilon (np.float64, optional): The softening parameter. Defaults to 1e-10.

    Returns:
        np.ndarray: The gravitational force between the two bodies.
    """
    mag = vector_magnitude_jit(r)
    if mag < epsilon:
        return np.zeros(3)
    return -G *((m1 * m2) / mag**2) * unit_vector_jit(r)

def timestep(t: np.float64, delta: np.float64) -> int:
    """
    Computes the time step.

    Args:
        t (np.float64): The current time.
        delta (np.float64): The frequency at which the simulation should be computed in seconds.

    Returns:
        int: The new time.
    """
    return int(t / delta)

def timesteps(limit: np.float64, delta: np.float64) -> int:
    """
    Computes the number of time steps.

    Args:
        limit (np.float64): The length of the simulation in seconds.
        delta (np.float64): The frequency at which the simulation should be computed in seconds.

    Returns:
        int: The number of time steps.
    """
    return int(limit / delta)

def safe_eval(expr):
    """Safely evaluate a basic math expression."""
    allowed_operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.BitXor: operator.xor,
        ast.USub: operator.neg,
    }

    def eval_node(node):
        if isinstance(node, ast.Num):  # <number>
            return node.n
        elif isinstance(node, ast.BinOp):  # <left> <operator> <right>
            return allowed_operators[type(node.op)](eval_node(node.left), eval_node(node.right))
        elif isinstance(node, ast.UnaryOp):  # <operator> <operand> e.g., -1
            return allowed_operators[type(node.op)](eval_node(node.operand))
        else:
            raise TypeError(node)

    node = ast.parse(expr, mode='eval').body
    return eval_node(node)

def interpret_time(string: str) -> np.float64:
    """Interprets a string as a time in seconds.

    Args:
        string (str): The string to interpret.

    Returns:
        float: The time in seconds.
    """
    if type(string) is float or type(string) is int: return string
    try:
        return safe_eval(string)
    except:
        units = {"s": 1, "min": 60, "hr": 3600, "d": 86400, "yr": 31536000}
        total_time = 0
        for part in string.split('+'):
            part = part.strip()
            for unit, factor in units.items():
                if part.endswith(unit):
                    part = part.removesuffix(unit)
                    total_time += float(part) * factor
                    break
            else:
                total_time += float(part)
        return total_time

def interpret_mass(string: str) -> np.float64:
    """Interprets a string as a mass in kilograms.

    Args:
        string (str): The string to interpret.

    Returns:
        float: The mass in kilograms.
    """
    if type(string) is float or type(string) is int: return string
    try:
        return safe_eval(string)
    except:
        units = {"kg": 1, "g": 1/1000, "t": 1000}
        total_mass = 0
        for part in string.split('+'):
            part = part.strip()
            for unit, factor in units.items():
                if part.endswith(unit):
                    part = part.removesuffix(unit)
                    total_mass += float(part) * factor
                    break
            else:
                total_mass += float(part)
        return total_mass

def interpret_distance(string: str) -> np.float64:
    """Interprets a string as a distance in meters.

    Args:
        string (str): The string to interpret.

    Returns:
        float: The distance in meters.
    """
    if type(string) is float or type(string) is int: return string
    try:
        return safe_eval(string)
    except:
        units = {"m": 1, "km": 1000, "cm": 1/100, "mm": 1/1000, "μm": 1/1000000, "nm": 1/1000000000}
        total_distance = 0
        for part in string.split('+'):
            part = part.strip()
            for unit, factor in units.items():
                if part.endswith(unit):
                    part = part.removesuffix(unit)
                    total_distance += float(part) * factor
                    break
            else:
                total_distance += float(part)
        return total_distance

def time_to(time: np.float64, unit: str, round_digits: int=-1) -> str:
    """Converts a time to a specific unit.

    Args:
        time (np.float64): The time to convert.
        unit (str): The unit to convert to.
        round_digits (int, optional): The number of digits to round to. Defaults to -1.

    Returns:
        str: The converted time.
    """
    if unit == "min":
        converted_time = time / 60
    elif unit == "hr":
        converted_time = time / 3600
    elif unit == "d":
        converted_time = time / 86400
    elif unit == "yr":
        converted_time = time / 31536000
    else:
        converted_time = time

    if round_digits >= 0:
        converted_time = round(converted_time, round_digits)

    return f"{converted_time}{unit}"

def mass_to(mass: np.float64, unit: str, round_digits: int=-1) -> str:
    """Converts a mass to a specific unit.

    Args:
        mass (np.float64): The mass to convert.
        unit (str): The unit to convert to.
        round_digits (int, optional): The number of digits to round to. Defaults to -1.

    Returns:
        str: The converted mass.
    """
    if unit == "g":
        converted_mass = mass * 1000
    elif unit == "t":
        converted_mass = mass / 1000
    else:
        converted_mass = mass

    if round_digits >= 0:
        converted_mass = round(converted_mass, round_digits)

    return f"{converted_mass}{unit}"

def distance_to(distance: np.float64, unit: str, round_digits: int=-1) -> str:
    """Converts a distance to a specific unit.

    Args:
        distance (np.float64): The distance to convert.
        unit (str): The unit to convert to.
        round_digits (int, optional): The number of digits to round to. Defaults to -1.

    Returns:
        str: The converted distance.
    """
    if unit == "km":
        converted_distance = distance / 1000
    elif unit == "cm":
        converted_distance = distance * 100
    elif unit == "mm":
        converted_distance = distance * 1000
    elif unit == "μm":
        converted_distance = distance * 1000000
    elif unit == "nm":
        converted_distance = distance * 1000000000
    else:
        converted_distance = distance

    if round_digits >= 0:
        converted_distance = round(converted_distance, round_digits)

    return f"{converted_distance}{unit}"

@njit
def clip_scalar(scalar, min, max):
    """
    Clips a scalar value between a minimum and maximum value.

    Args:
        scalar (float): The scalar value to clip.
        min (float): The minimum value.
        max (float): The maximum value.

    Returns:
        float: The clipped scalar value.
    """
    if scalar < min: return min
    if scalar > max: return max
    return scalar

def state(body, n):
    return body._inner["r"][n], body._inner["v"][n]

def round_limit(limit, delta):
    return round(limit / delta) * delta

def round_time(t, delta):
    return round(t / delta) * delta

@njit
def gravitational_forces(bodies, body, i, n):
    f = np.zeros(3)
    for j, other in enumerate(bodies):
        if i != j: f += ax.gravitational_force_jit(body["m"], other["m"], body["r"][n] - other["r"][n])
    return f

@njit 
def locate_body(body, bodies):
    for i, b in enumerate(bodies):
        if b["n"] == body["n"]:
            return i
    return -1