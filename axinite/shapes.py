import trimesh

def create_sphere(radius=1.0):
    sphere = trimesh.creation.icosphere(subdivisions=4, radius=radius)
    return sphere

def create_cube(size=1.0):
    cube = trimesh.creation.box(extents=[size, size, size])
    return cube

def create_rectangle(width=1.0, height=1.0):
    rectangle = trimesh.creation.box(extents=[width, height, 0.01])
    return rectangle