import axinite as ax
import axinite.analysis as axana
import numpy as np
from numba import jit

@jit
def _kinetic_energy_at(n: np.float64, bodies: np.ndarray):
    """
    Calculate the kinetic energy at a specific time step for an array of bodies.

    Args:
        n (np.float64): The time step index.
        bodies (np.ndarray): Array of body dictionaries with mass and velocity.

    Returns:
        float: The kinetic energy at the specified time step.
    """
    kinetic_energy = 0
    for body in bodies:
        kinetic_energy += 0.5 * body["m"] * np.linalg.norm(body["v"][n]) ** 2
    return kinetic_energy

def kinetic_energy_at(n: np.float64, bodies: list[ax.Body]):
    """
    Calculate the kinetic energy at a specific time step for a list of bodies.

    Args:
        n (np.float64): The time step index.
        bodies (list[ax.Body]): List of Body objects.

    Returns:
        float: The kinetic energy at the specified time step.
    """
    return _kinetic_energy_at(n, ax.get_inner_bodies(bodies))

@jit
def _total_kinetic_energy_at(n: np.float64, bodies: np.ndarray):
    """
    Calculate the total kinetic energy at a specific time step for an array of bodies.

    Args:
        n (np.float64): The time step index.
        bodies (np.ndarray): Array of body dictionaries with mass and velocity.

    Returns:
        float: The total kinetic energy at the specified time step.
    """
    return np.sum(_kinetic_energy_at(n, bodies))

def total_kinetic_energy_at(n: np.float64, bodies: list[ax.Body]):
    """
    Calculate the total kinetic energy at a specific time step for a list of bodies.

    Args:
        n (np.float64): The time step index.
        bodies (list[ax.Body]): List of Body objects.

    Returns:
        float: The total kinetic energy at the specified time step.
    """
    return _total_kinetic_energy_at(n, ax.get_inner_bodies(bodies))

@jit
def _kinetic_energy(bodies: np.ndarray):
    """
    Calculate the kinetic energy over all time steps for an array of bodies.

    Args:
        bodies (np.ndarray): Array of body dictionaries with mass and velocity.

    Returns:
        np.ndarray: Array of kinetic energies for each time step.
    """
    kinetic_energies = np.zeros(bodies[0]["r"].shape[0])
    n = 0
    while n < bodies[0]["r"].shape[0]:
        kinetic_energies[n] = _kinetic_energy_at(n, bodies)
        n += 1
    return kinetic_energies

def kinetic_energy(bodies: list[ax.Body]):
    """
    Calculate the kinetic energy over all time steps for a list of bodies.

    Args:
        bodies (list[ax.Body]): List of Body objects.

    Returns:
        np.ndarray: Array of kinetic energies for each time step.
    """
    return _kinetic_energy(ax.get_inner_bodies(bodies))

@jit
def _total_kinetic_energy(bodies: np.ndarray):
    """
    Calculate the total kinetic energy over all time steps for an array of bodies.

    Args:
        bodies (np.ndarray): Array of body dictionaries with mass and velocity.

    Returns:
        float: The total kinetic energy over all time steps.
    """
    return np.sum(_kinetic_energy(bodies))

def total_kinetic_energy(bodies: list[ax.Body]):
    """
    Calculate the total kinetic energy over all time steps for a list of bodies.

    Args:
        bodies (list[ax.Body]): List of Body objects.

    Returns:
        float: The total kinetic energy over all time steps.
    """
    return _total_kinetic_energy(ax.get_inner_bodies(bodies))

@jit
def _potential_energy_at(n: np.float64, bodies: np.ndarray):
    """
    Calculate the potential energy at a specific time step for an array of bodies.

    Args:
        n (np.float64): The time step index.
        bodies (np.ndarray): Array of body dictionaries with mass and position.

    Returns:
        float: The potential energy at the specified time step.
    """
    potential_energy = 0
    for i in range(len(bodies)):
        for j in range(i + 1, len(bodies)):
            distance = np.linalg.norm(bodies[i]["r"][n] - bodies[j]["r"][n])
            if distance > 0: 
                potential_energy -= ax.G * bodies[i]["m"] * bodies[j]["m"] / distance
    return potential_energy

def potential_energy_at(n: np.float64, bodies: list[ax.Body]):
    """
    Calculate the potential energy at a specific time step for a list of bodies.

    Args:
        n (np.float64): The time step index.
        bodies (list[ax.Body]): List of Body objects.

    Returns:
        float: The potential energy at the specified time step.
    """
    return _potential_energy_at(n, ax.get_inner_bodies(bodies))

@jit
def _total_potential_energy_at(n: np.float64, bodies: np.ndarray):
    """
    Calculate the total potential energy at a specific time step for an array of bodies.

    Args:
        n (np.float64): The time step index.
        bodies (np.ndarray): Array of body dictionaries with mass and position.

    Returns:
        float: The total potential energy at the specified time step.
    """
    return np.sum(_potential_energy_at(n, bodies))

def total_potential_energy_at(n: np.float64, bodies: list[ax.Body]):
    """
    Calculate the total potential energy at a specific time step for a list of bodies.

    Args:
        n (np.float64): The time step index.
        bodies (list[ax.Body]): List of Body objects.

    Returns:
        float: The total potential energy at the specified time step.
    """
    return _total_potential_energy_at(n, ax.get_inner_bodies(bodies))

@jit
def _potential_energy(bodies: np.ndarray):
    """
    Calculate the potential energy over all time steps for an array of bodies.

    Args:
        bodies (np.ndarray): Array of body dictionaries with mass and position.

    Returns:
        np.ndarray: Array of potential energies for each time step.
    """
    potential_energies = np.zeros(bodies[0]["r"].shape[0])
    n = 0
    while n < bodies[0]["r"].shape[0]:
        potential_energies[n] = _potential_energy_at(n, bodies)
        n += 1
    return potential_energies

def potential_energy(bodies: list[ax.Body]):
    """
    Calculate the potential energy over all time steps for a list of bodies.

    Args:
        bodies (list[ax.Body]): List of Body objects.

    Returns:
        np.ndarray: Array of potential energies for each time step.
    """
    return _potential_energy(ax.get_inner_bodies(bodies))

@jit
def _total_potential_energy(bodies: np.ndarray):
    """
    Calculate the total potential energy over all time steps for an array of bodies.

    Args:
        bodies (np.ndarray): Array of body dictionaries with mass and position.

    Returns:
        float: The total potential energy over all time steps.
    """
    return np.sum(_potential_energy(bodies))

def total_potential_energy(bodies: list[ax.Body]):
    """
    Calculate the total potential energy over all time steps for a list of bodies.

    Args:
        bodies (list[ax.Body]): List of Body objects.

    Returns:
        float: The total potential energy over all time steps.
    """
    return _total_potential_energy(ax.get_inner_bodies(bodies))

@jit
def _energy_at(n: np.float64, bodies: np.ndarray):
    """
    Calculate the total energy (kinetic + potential) at a specific time step for an array of bodies.

    Args:
        n (np.float64): The time step index.
        bodies (np.ndarray): Array of body dictionaries with mass, velocity, and position.

    Returns:
        float: The total energy at the specified time step.
    """
    return _kinetic_energy_at(n, bodies) + _potential_energy_at(n, bodies)

def energy_at(n: np.float64, bodies: list[ax.Body]):
    """
    Calculate the total energy (kinetic + potential) at a specific time step for a list of bodies.

    Args:
        n (np.float64): The time step index.
        bodies (list[ax.Body]): List of Body objects.

    Returns:
        float: The total energy at the specified time step.
    """
    return _energy_at(n, ax.get_inner_bodies(bodies))

@jit
def _total_energy_at(n: np.float64, bodies: np.ndarray):
    """
    Calculate the total energy (total kinetic + total potential) at a specific time step for an array of bodies.

    Args:
        n (np.float64): The time step index.
        bodies (np.ndarray): Array of body dictionaries with mass, velocity, and position.

    Returns:
        float: The total energy at the specified time step.
    """
    return _total_kinetic_energy_at(n, bodies) + _total_potential_energy_at(n, bodies)

def total_energy_at(n: np.float64, bodies: list[ax.Body]):
    """
    Calculate the total energy (total kinetic + total potential) at a specific time step for a list of bodies.

    Args:
        n (np.float64): The time step index.
        bodies (list[ax.Body]): List of Body objects.

    Returns:
        float: The total energy at the specified time step.
    """
    return _total_energy_at(n, ax.get_inner_bodies(bodies))

@jit
def _energy(bodies: np.ndarray):
    """
    Calculate the total energy (kinetic + potential) over all time steps for an array of bodies.

    Args:
        bodies (np.ndarray): Array of body dictionaries with mass, velocity, and position.

    Returns:
        np.ndarray: Array of total energies for each time step.
    """
    return _kinetic_energy(bodies) + _potential_energy(bodies)

def energy(bodies: list[ax.Body]):
    """
    Calculate the total energy (kinetic + potential) over all time steps for a list of bodies.

    Args:
        bodies (list[ax.Body]): List of Body objects.

    Returns:
        np.ndarray: Array of total energies for each time step.
    """
    return _energy(ax.get_inner_bodies(bodies))

@jit
def _total_energy(bodies: np.ndarray):
    """
    Calculate the total energy (total kinetic + total potential) over all time steps for an array of bodies.

    Args:
        bodies (np.ndarray): Array of body dictionaries with mass, velocity, and position.

    Returns:
        float: The total energy over all time steps.
    """
    return _total_kinetic_energy(bodies) + _total_potential_energy(bodies)

def total_energy(bodies: list[ax.Body]):
    """
    Calculate the total energy (total kinetic + total potential) over all time steps for a list of bodies.

    Args:
        bodies (list[ax.Body]): List of Body objects.

    Returns:
        float: The total energy over all time steps.
    """
    return _total_energy(ax.get_inner_bodies(bodies))

def kinetic_energy_of(body: ax.Body):
    """
    Calculate the kinetic energy over all time steps for a single body.

    Args:
        body (ax.Body): A Body object.

    Returns:
        np.ndarray: Array of kinetic energies for each time step.
    """
    inner_body = ax.get_inner_body(body)
    kinetic_energies = np.zeros(inner_body["r"].shape[0])
    for n in range(inner_body["r"].shape[0]):
        kinetic_energies[n] = 0.5 * inner_body["m"] * np.linalg.norm(inner_body["v"][n]) ** 2
    return kinetic_energies

def potential_energy_of(body: ax.Body, other_bodies: list[ax.Body]):
    """
    Calculate the potential energy over all time steps for a single body with respect to other bodies.

    Args:
        body (ax.Body): A Body object.
        other_bodies (list[ax.Body]): List of other Body objects.

    Returns:
        np.ndarray: Array of potential energies for each time step.
    """
    inner_body = ax.get_inner_body(body)
    inner_other_bodies = ax.get_inner_bodies(other_bodies)
    potential_energies = np.zeros(inner_body["r"].shape[0])
    for n in range(inner_body["r"].shape[0]):
        potential_energy = 0
        for other_body in inner_other_bodies:
            distance = np.linalg.norm(inner_body["r"][n] - other_body["r"][n])
            if distance > 0:
                potential_energy -= ax.G * inner_body["m"] * other_body["m"] / distance
        potential_energies[n] = potential_energy
    return potential_energies

def total_energy_of(body: ax.Body, other_bodies: list[ax.Body]):
    """
    Calculate the total energy (kinetic + potential) over all time steps for a single body with respect to other bodies.

    Args:
        body (ax.Body): A Body object.
        other_bodies (list[ax.Body]): List of other Body objects.

    Returns:
        np.ndarray: Array of total energies for each time step.
    """
    kinetic_energies = kinetic_energy_of(body)
    potential_energies = potential_energy_of(body, other_bodies)
    return kinetic_energies + potential_energies