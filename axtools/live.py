import axinite as ax
from axtools import AxiniteArgs, to_vec
from vpython import *
from itertools import cycle
import vpython as vp

colors = cycle([color.red, color.blue, color.green, color.orange, color.purple, color.yellow])

def live(limit, delta, t, *bodies: ax.Body, radius_multiplier=1, rate=100, retain=200):
    if rate is None:
        rate = 100
    if radius_multiplier is None:
        radius_multiplier = 1
    if retain is None:
        retain = 200

    scene = canvas()
    scene.select()

    spheres = {}
    labels = {}

    for body in bodies:
        spheres[body.name] = sphere(pos=to_vec(body.r[0]), radius=body.radius.value * radius_multiplier, color=next(colors), make_trail=True, retain=retain, interval=10)
        labels[body.name] = label(pos=spheres[body.name].pos, text=body.name, xoffset=15, yoffset=15, space=30, height=10, border=4, font='sans')

    def fn(t, **kwargs):
        vp.rate(rate)
        for body in kwargs["bodies"]:
            spheres[body.name].pos = to_vec(body.r[t.value])
            labels[body.name].pos = spheres[body.name].pos
        print(f"t = {t}", end='\r')

    ax.load(delta, limit, fn, *bodies, t=t)