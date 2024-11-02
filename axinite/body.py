from misura.quantities import quantity
from trimesh import Trimesh
from axinite.vector import Vector3

class Body:
    def __init__(self, name: str, mass: quantity, position: Vector3, velocity: quantity, mesh: Trimesh):
        self.name = name
        self.mass = mass
        self.position = position
        self.velocity = velocity
        self.mesh = Trimesh
        
    def gravitational_force(self, other):
        G = quantity(6.67430e-11, 'm3 kg-1 s-2')
        return G * ((self.mass * other.mass) / (abs(self.position - other.position)))