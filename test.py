from axinite import Body, Vector3
from misura.quantities import quantity
from trimesh import Trimesh

A = Body(
    "A", 
    quantity(5.972e24, "kg"),  # mass of the Earth
    Vector3(quantity(0, "km"), quantity(0, "km"), quantity(0, "km")), 
    quantity(0, "m s-1"),
    Trimesh()
)
B = Body(
    "B", 
    quantity(7.342e22, "kg"),  # mass of the moon
    Vector3(quantity(384400, "km"), quantity(0, "km"), quantity(0, "km")),  # average distance from Earth to Moon in km
    quantity(1.022, "km s-1"),  # average orbital speed of the moon
    Trimesh()
)

print(A.mass, A.position, A.velocity)
print(B.mass, B.position, B.velocity)
print(A.gravitational_force(B))