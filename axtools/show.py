import axinite as ax
from vpython import *
from axtools import to_vec, to_float
from itertools import cycle

colors = cycle([color.red, color.blue, color.green, color.orange, color.purple, color.yellow])

def show(limit, delta, *bodies: ax.Body, radius_multiplier=1, speed=100, retain=200):
    scene = canvas()
    scene.select()

    spheres = {}
    labels = {}
    
    for body in bodies:
        spheres[body.name] = sphere(pos=to_vec(body.r[0]), radius=body.radius.value * radius_multiplier, color=next(colors), make_trail=True, retain=retain, interval=10)
        labels[body.name] = label(pos=spheres[body.name].pos, text=body.name, xoffset=15, yoffset=15, space=30, height=10, border=4, font='sans')
    
    t = to_float(0)
    print(t, limit)
    while t < limit:
        rate(speed)
        for body in bodies:
            spheres[body.name].pos = to_vec(body.r[t])
            labels[body.name].pos = spheres[body.name].pos
        t += delta
        print(f"t = {t}", end='\r')



    