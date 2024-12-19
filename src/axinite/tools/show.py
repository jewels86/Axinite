import axinite as ax
from vpython import *
from axinite.tools import to_vec, to_float, string_to_color, Body
from itertools import cycle
import vpython as vp

colors = cycle([color.red, color.blue, color.green, color.orange, color.purple, color.yellow])

def show(_args):
    args = _args
    if args.rate is None:
        args.rate = 100
    if args.radius_multiplier is None:
        args.radius_multiplier = 1
    if args.retain is None:
        args.retain = 200

    global pause
    pause = False
    global _rate
    _rate = args.rate
    
    scene = canvas()
    scene.select()
    if args.name: scene.title = args.name

    def pause_fn():
        global pause
        pause = not pause
    def rate_change_fn(evt):
        global _rate
        _rate = int(evt.value)

    pause_btn = button(bind=pause_fn, text='Pause', pos=scene.caption_anchor)
    rate_slider = slider(bind=rate_change_fn, min=1, max=1000, value=_rate, step=5, pos=scene.caption_anchor, length=200)

    spheres = {}
    labels = {}
    
    for body in args.bodies:
        body_color = string_to_color(body.color) if body.color != "" else next(colors)
        body_retain = body.retain if body.retain != None else args.retain
        spheres[body.name] = sphere(pos=to_vec(body.r[0]), radius=body.radius.value * args.radius_multiplier, color=body_color, make_trail=True, retain=body_retain, interval=10)
        labels[body.name] = label(pos=spheres[body.name].pos, text=body.name, xoffset=15, yoffset=15, space=30, height=10, border=4, font='sans')
    
    t = to_float(0)
    while t < args.limit:
        vp.rate(_rate)
        for body in args.bodies:
            spheres[body.name].pos = to_vec(body.r[t])
            labels[body.name].pos = spheres[body.name].pos
        t += args.delta
        print(f"t = {t}", end='\r')
        while pause: vp.rate(10)



