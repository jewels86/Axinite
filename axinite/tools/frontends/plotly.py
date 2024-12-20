import axinite.tools as axtools
import plotly.graph_objects as go
from itertools import cycle
from astropy.coordinates import CartesianRepresentation

def to_vec(cartesian_representation: CartesianRepresentation):
    return dict(x=cartesian_representation.x.value, y=cartesian_representation.y.value, z=cartesian_representation.z.value)

def plotly_frontend(args: axtools.AxiniteArgs):
    colors = cycle(['red', 'blue', 'green', 'orange', 'purple', 'yellow'])
    global pause
    pause = False

    fig = go.Figure()
    if args.name: fig.update_layout(title=args.name)

    spheres = {}
    labels = {}

    for body in args.bodies:
        body_color = body.color, "plotly" if body.color != "" else next(colors)
        body_retain = body.retain if body.retain != None else args.retain
        spheres[body.name] = go.Scatter3d(x=[body.r[0].x.value], y=[body.r[0].y.value], z=[body.r[0].z.value], mode='markers+lines', marker=dict(size=body.radius.value * args.radius_multiplier, color=body_color))
        labels[body.name] = go.Scatter3d(x=[body.r[0].x.value], y=[body.r[0].y.value], z=[body.r[0].z.value], mode='text', text=[body.name], textposition='top center')
        fig.add_trace(spheres[body.name])
        fig.add_trace(labels[body.name])

    def fn(t, **kwargs):
        for body in kwargs["bodies"]:
            spheres[body.name].x = [body.r[t.value].x.value]
            spheres[body.name].y = [body.r[t.value].y.value]
            spheres[body.name].z = [body.r[t.value].z.value]
            labels[body.name].x = [body.r[t.value].x.value]
            labels[body.name].y = [body.r[t.value].y.value]
            labels[body.name].z = [body.r[t.value].z.value]
        fig.show()
        print(f"t = {t}", end='\r')
        if pause: 
            while pause: pass
            
    return fn
