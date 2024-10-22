from axinite.units import Volume, Mass, Km, Km2, Km3, Kg, Celsius, mPs, s
from axinite.quantities import Vector3
from axinite.formulas import escape_velocity
from trimesh import Trimesh
import numpy as np

class Body:
    def __init__(self, label: str, mesh: Trimesh, position: Vector3, volume: Volume = Km3(), mass: Mass = Kg()):
        """
        Initializes a new celestial body.
        
        Args:
        - `label` (`str`): The name of the body.
        - `mesh` (`Trimesh`): The model for the body to be rendered with.
        - `position` (`Vector3`): The body's initial position.
        - `volume` (`Volume`): The body's volume in `Volume` units.
        - `mass` (`Mass`): The body's mass in `Mass` units.
        """
        self.label = label
        self.mesh = mesh
        self.position = position
        self.volume = volume
        self.mass = mass
        
        self.density = mass / volume
        self.radius = Km(0)
        self.area = Km2(0)
        self.temperature = Celsius(0)
        self.escape_velocity = escape_velocity(self.mass + Kg(0), self.radius)
        self.age = s(0)
        
        scale = (self.volume.value / mesh.volume) ** 1/3
        
        center = mesh.center_mass
        distances = np.linalg.norm(mesh.vertices - center, axis=1)
        self.radius = Km(np.mean(distances) * scale)