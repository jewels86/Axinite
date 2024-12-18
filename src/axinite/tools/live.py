import axinite as ax
from axinite.tools import AxiniteArgs, to_vec, Body, string_to_color
from vpython import *
from itertools import cycle
import vpython as vp

colors = cycle([color.red, color.blue, color.green, color.orange, color.purple, color.yellow])

def live(limit, delta, t, *bodies: Body, radius_multiplier=1, rate=100, retain=200, name=None):
    if rate is None:
        rate = 100
    if radius_multiplier is None:
        radius_multiplier = 1
    if retain is None:
        retain = 200

    global pause
    pause = False

    scene = canvas()
    scene.select()
    if name: scene.title = name

    def pause_fn():
        global pause
        pause = not pause

    pause_btn = button(bind=pause_fn, text='Pause', pos=scene.caption_anchor)

    spheres = {}
    labels = {}
    lights = {}

    for body in bodies:
        body_color = string_to_color(body.color) if body.color != "" else next(colors)
        body_retain = body.retain if body.retain != None else retain
        spheres[body.name] = sphere(pos=to_vec(body.r[0]), radius=body.radius.value * radius_multiplier, color=body_color, make_trail=True, retain=body_retain, interval=10)
        labels[body.name] = label(pos=spheres[body.name].pos, text=body.name, xoffset=15, yoffset=15, space=30, height=10, border=4, font='sans')
        if body.light == True: lights[body.name] = local_light(pos=to_vec(body.r[0]), color=body_color)

    def fn(t, **kwargs):
        vp.rate(rate)
        for body in kwargs["bodies"]:
            spheres[body.name].pos = to_vec(body.r[t.value])
            labels[body.name].pos = spheres[body.name].pos
            try: lights[body.name].pos = spheres[body.name].pos
            except: pass
        print(f"t = {t}", end='\r')
        if pause: 
            while pause: vp.rate(10)

    ax.load(delta, limit, fn, *bodies, t=t)