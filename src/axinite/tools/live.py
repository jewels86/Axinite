import axinite as ax
from axinite.tools import AxiniteArgs, to_vec, Body, string_to_color
from vpython import *
from itertools import cycle

colors = cycle([color.red, color.blue, color.green, color.orange, color.purple, color.yellow])

def live(_args: AxiniteArgs):
    args = _args
    if args.rate is None:
        args.rate = 100
    if args.radius_multiplier is None:
        args.radius_multiplier = 1
    if args.retain is None:
       args.retain = 200

    global pause
    pause = False

    scene = canvas()
    scene.select()
    if args.name: scene.title = args.name

    def pause_fn():
        global pause
        pause = not pause

    pause_btn = button(bind=pause_fn, text='Pause', pos=scene.caption_anchor)

    spheres = {}
    labels = {}
    lights = {}

    for body in args.bodies:
        body_color = string_to_color(body.color) if body.color != "" else next(colors)
        body_retain = body.retain if body.retain != None else args.retain
        spheres[body.name] = sphere(pos=to_vec(body.r[0]), radius=body.radius.value * args.radius_multiplier, color=body_color, make_trail=True, retain=body_retain, interval=10)
        labels[body.name] = label(pos=spheres[body.name].pos, text=body.name, xoffset=15, yoffset=15, space=30, height=10, border=4, font='sans')
        if body.light == True: lights[body.name] = local_light(pos=to_vec(body.r[0]), color=body_color)

    def fn(t, **kwargs):
        rate(args.rate)
        for body in kwargs["bodies"]:
            spheres[body.name].pos = to_vec(body.r[t.value])
            labels[body.name].pos = spheres[body.name].pos
            try: lights[body.name].pos = spheres[body.name].pos
            except: pass
        print(f"t = {t}", end='\r')
        if pause: 
            while pause: rate(10)

    args.function = fn
    ax.load(*args.unpack(), t=args.t)