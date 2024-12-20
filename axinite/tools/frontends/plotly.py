import axinite.tools as axtools
import plotly.graph_objects as go
import plotly
from itertools import cycle
from astropy.coordinates import CartesianRepresentation

def plotly_rt_frontend(args: axtools.AxiniteArgs, theme="plotly_dark"):
    """A plotly frontend for a real-time visualization of the simulation.

    Args:
        args (axtools.AxiniteArgs): The arguments for the simulation.
    """
    colors = cycle(['red', 'blue', 'green', 'orange', 'purple', 'yellow'])
    global pause
    pause = False
    
    figure = go.Figure()
    layout = go.Layout(
        autosize=True,
        template=theme,
        scene=dict(
            xaxis=dict(title='X'),
            yaxis=dict(title='Y'),
            zaxis=dict(title='Z')
        )
    )
    figure.update_layout(layout)
    
    spheres = {}

    for body in args.bodies:
        body_color = body.color if body.color != "" else next(colors)
        print(body.r[0], body.radius)
        xx, yy, zz = axtools.create_sphere(body.r[0], body.radius)
        spheres[body.name] = go.Surface(
            x=xx,
            y=yy,
            z=zz,
            colorscale=[[0, body_color], [1, body_color]],
            cauto=False,
            cmin=1,
            cmax=1,
            showlegend=True,
            showscale=False,
            name=body.name,
        )
        figure.add_trace(spheres[body.name])
    
    def fn(t, bodies=list(args.bodies), **kwargs):
        for body in bodies:
            xx, yy, zz = axtools.create_sphere(body.r[t.value], body.radius)
            spheres[body.name].update(x=xx, y=yy, z=zz)
        figure.update_traces()
    
    figure.show()
    return fn