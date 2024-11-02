import trimesh

def create_circle(radius=1.0, segments=32):
    circle = trimesh.creation.disk(radius=radius, segments=segments)
    return circle

def create_cube(size=1.0):
    cube = trimesh.creation.box(extents=[size, size, size])
    return cube

def create_rectangle(width=1.0, height=1.0):
    rectangle = trimesh.creation.box(extents=[width, height, 0.01])
    return rectangle