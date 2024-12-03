import axinite as ax
from vpython import *
from lite import to_vec
from itertools import cycle

colors = cycle([color.red, color.blue, color.green, color.orange, color.purple, color.yellow])

def show(limit, *bodies: ax.Body):
    scene = canvas(width=1200, height=800, background=color.black)
    scene.select()

    spheres = {}
    trails = {}
    labels = {}
    
    for body in bodies:
        spheres[body.name] = sphere(pos=to_vec(body.r[0]), radius=body.radius, color=next(colors))
        trails[body.name] = curve(color=spheres[body.name].color)
        labels[body.name] = label(pos=spheres[body.name].pos, text=body.name, xoffset=15, yoffset=15, space=30, height=10, border=4, font='sans')
    
    t = 0
    while t < limit:
        rate(60)
        for body in bodies:
            spheres[body.name].pos = to_vec(body.r[t])
            trails[body.name].append(pos=spheres[body.name].pos)
            labels[body.name].pos = spheres[body.name].pos
        t += 1


    