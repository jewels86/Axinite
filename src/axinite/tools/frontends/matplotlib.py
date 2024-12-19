import axinite.tools as axtools
from vpython import *
from itertools import cycle
from matplotlib.pyplot import *

class MPLFrontend(axtools.Frontend):
    def __init__(self):
        super().__init__()
        
    def run(self, args: axtools.AxiniteArgs):
        colors = cycle(['r', 'b', 'g', 'orange', 'purple', 'yellow'])
        global _pause
        _pause = False

        fig = figure()
        ax = fig.add_subplot(111, projection='3d')
        if args.name: fig.suptitle(args.name)

        def pause_fn(event):
            global _pause
            _pause = not _pause

        fig.canvas.mpl_connect('key_press_event', pause_fn)

        spheres = {}
        labels = {}
        lights = {}

        for body in args.bodies:
            body_color = body.color if body.color != "" else next(colors)
            body_retain = body.retain if body.retain != None else args.retain
            spheres[body.name] = ax.scatter([body.r[0][0]], [body.r[0][1]], [body.r[0][2]], s=body.radius.value * args.radius_multiplier, c=body_color)
            labels[body.name] = ax.text(body.r[0][0], body.r[0][1], body.r[0][2], body.name)
            if body.light == True: lights[body.name] = axtools.to_vec(body.r[0])

        def fn(t, **kwargs):
            for body in kwargs["bodies"]:
                spheres[body.name]._offsets3d = (body.r[t.value][0], body.r[t.value][1], body.r[t.value][2])
                labels[body.name].set_position((body.r[t.value][0], body.r[t.value][1], body.r[t.value][2]))
                #try: lights[body.name] = axtools.to_vec(body.r[t.value])
                #except: pass
        
        return fn