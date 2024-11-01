from misura.quantities import quantity
from trimesh import Trimesh

class Body:
    def __init__(self, mesh: Trimesh, mass: quantity, volume: quantity, label: str, ):
        self.mesh = mesh.apply_scale((volume / mesh.volume) ** (1/3))
        
        self.mass = mass
        self.volume = volume
        self.density = mass / volume
        
        self.average_radius = (mesh.bounding_sphere.primitive.radius + mesh.bounding_box_oriented.primitive.extents.max() / 2) / 2
        self.label = label