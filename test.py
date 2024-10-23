from axinite import Body, Vector3, Km3, Kg, e, formulas
from trimesh import Trimesh

primary = Body("primary", Trimesh(), Vector3(0, 0, 0), Km3(e(1.083, 12)), Kg(e(5.97, 24)))
secondary = Body("secondary", Trimesh(), Vector3(1, 1, 1), Km3(e(1.083, 12)), Kg(e(5.97, 24)))

print(primary.escape_velocity)