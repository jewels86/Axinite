import axinite as ax
from vpython import *
from axtools import to_vec, to_float, string_to_color
from itertools import cycle
import axtools

colors = cycle([color.red, color.blue, color.green, color.orange, color.purple, color.yellow])

def show(limit, delta, *bodies: axtools.Body, radius_multiplier=1, speed=100, retain=200):
    if speed is None:
        speed = 100
    if radius_multiplier is None:
        radius_multiplier = 1
    if retain is None:
        retain = 200
    
    scene = canvas()
    scene.select()

    spheres = {}
    labels = {}
    
    for body in bodies:
        body_color = string_to_color(body.color) if body.color != "" else next(colors)
        body_retain = body.retain if body.retain != None else retain
        spheres[body.name] = sphere(pos=to_vec(body.r[0]), radius=body.radius.value * radius_multiplier, color=body_color, make_trail=True, retain=body_retain, interval=10)
        labels[body.name] = label(pos=spheres[body.name].pos, text=body.name, xoffset=15, yoffset=15, space=30, height=10, border=4, font='sans')
    
    t = to_float(0)
    while t < limit:
        rate(speed)
        for body in bodies:
            spheres[body.name].pos = to_vec(body.r[t])
            labels[body.name].pos = spheres[body.name].pos
        t += delta
        print(f"t = {t}", end='\r')



