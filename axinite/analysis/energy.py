import axinite as ax
import axinite.analysis as axana
import numpy as np
from numba import jit

@jit
def _kinetic_energy_at(n: np.float64, bodies: np.ndarray):
    kinetic_energy = 0
    for body in bodies:
        kinetic_energy += 0.5 * body["m"] * np.linalg.norm(body["v"][n]) ** 2
    return kinetic_energy

def kinetic_energy_at(n: np.float64, bodies: list[ax.Body]):
    return _kinetic_energy_at(n, ax.get_inner_bodies(bodies))

@jit
def _total_kinetic_energy_at(n: np.float64, bodies: np.ndarray):
    return np.sum(_kinetic_energy_at(n, bodies))

def total_kinetic_energy_at(n: np.float64, bodies: list[ax.Body]):
    return _total_kinetic_energy_at(n, ax.get_inner_bodies(bodies))

@jit
def _kinetic_energy(bodies: np.ndarray):
    kinetic_energies = np.zeros(bodies[0]["r"].shape[0])
    n = 0
    while n < bodies[0]["r"].shape[0]:
        kinetic_energies[n] = _kinetic_energy_at(n, bodies)
        n += 1
    return kinetic_energies

def kinetic_energy(bodies: list[ax.Body]):
    return _kinetic_energy(ax.get_inner_bodies(bodies))

@jit
def _total_kinetic_energy(bodies: np.ndarray):
    return np.sum(_kinetic_energy(bodies))

def total_kinetic_energy(bodies: list[ax.Body]):
    return _total_kinetic_energy(ax.get_inner_bodies(bodies))

@jit
def _potential_energy_at(n: np.float64, bodies: np.ndarray):
    potential_energy = 0
    for i in range(len(bodies)):
        for j in range(i + 1, len(bodies)):
            distance = np.linalg.norm(bodies[i]["r"][n] - bodies[j]["r"][n])
            potential_energy -= ax.G * bodies[i]["m"] * bodies[j]["m"] / distance
    return potential_energy

def potential_energy_at(n: np.float64, bodies: list[ax.Body]):
    return _potential_energy_at(n, ax.get_inner_bodies(bodies))

@jit
def _total_potential_energy_at(n: np.float64, bodies: np.ndarray):
    return np.sum(_potential_energy_at(n, bodies))

def total_potential_energy_at(n: np.float64, bodies: list[ax.Body]):
    return _total_potential_energy_at(n, ax.get_inner_bodies(bodies))

@jit
def _potential_energy(bodies: np.ndarray):
    potential_energies = np.zeros(bodies[0]["r"].shape[0])
    n = 0
    while n < bodies[0]["r"].shape[0]:
        potential_energies[n] = _potential_energy_at(n, bodies)
        n += 1
    return potential_energies

def potential_energy(bodies: list[ax.Body]):
    return _potential_energy(ax.get_inner_bodies(bodies))

@jit
def _total_potential_energy(bodies: np.ndarray):
    return np.sum(_potential_energy(bodies))

def total_potential_energy(bodies: list[ax.Body]):
    return _total_potential_energy(ax.get_inner_bodies(bodies))

@jit
def _energy_at(n: np.float64, bodies: np.ndarray):
    return _kinetic_energy_at(n, bodies) + _potential_energy_at(n, bodies)

def energy_at(n: np.float64, bodies: list[ax.Body]):
    return _energy_at(n, ax.get_inner_bodies(bodies))

@jit
def _total_energy_at(n: np.float64, bodies: np.ndarray):
    return _total_kinetic_energy_at(n, bodies) + _total_potential_energy_at(n, bodies)

def total_energy_at(n: np.float64, bodies: list[ax.Body]):
    return _total_energy_at(n, ax.get_inner_bodies(bodies))

@jit
def _energy(bodies: np.ndarray):
    return _kinetic_energy(bodies) + _potential_energy(bodies)

def energy(bodies: list[ax.Body]):
    return _energy(ax.get_inner_bodies(bodies))

@jit
def _total_energy(bodies: np.ndarray):
    return _total_kinetic_energy(bodies) + _total_potential_energy(bodies)

def total_energy(bodies: list[ax.Body]):
    return _total_energy(ax.get_inner_bodies(bodies))