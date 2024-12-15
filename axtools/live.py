import axinite as ax
from axtools import AxiniteArgs, to_vec
from vpython import *

def live(args: AxiniteArgs):
    scene = canvas()
    scene.select()

    spheres = {}
    labels = {}

    for body in args.bodies:
        spheres[body.name] = sphere(pos=to_vec(body.r[0]), radius=body.radius.value * args.radius_multiplier, color=body.color, make_trail=True, retain=args.retain, interval=10)
        labels[body.name] = label(pos=spheres[body.name].pos, text=body.name, xoffset=15, yoffset=15, space=30, height=10, border=4, font='sans')

    def fn(t, bodies, **kwargs):
        rate(args.rate)
        for body in bodies:
            spheres[body.name].pos = to_vec(body.r[t])
            labels[body.name].pos = spheres[body.name].pos
        print(f"t = {t}", end='\r')

    ax.load(args.delta, args.limit, fn, args.bodies, t=args.t)