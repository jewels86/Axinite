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

    max_len = axtools.max_axis_length(*args.bodies, radius_multiplier=args.radius_multiplier)
    min_len = axtools.min_axis_length(*args.bodies, radius_multiplier=args.radius_multiplier)
    
    figure = go.Figure()
    layout = go.Layout(
        autosize=True,
        template=theme,
        scene=dict(
            aspectmode='cube',
            xaxis=dict(title='X', range=[-max_len, max_len]),
            yaxis=dict(title='Y', range=[-max_len, max_len]),
            zaxis=dict(title='Z', range=[-max_len, max_len]),
        )
    )
    f2 = go.FigureWidget(figure)
    figure.update_layout(layout)
    
    spheres = {}
    labels = {}
    trails = {k.name: {'x': [], 'y': [], 'z': []} for k in args.bodies}


    for body in args.bodies:
        body_color = body.color if body.color != "" else next(colors)
        xx, yy, zz = axtools.create_sphere(body.r[0], body.radius * args.radius_multiplier)
        spheres[body.name] = go.Surface(
            x=xx,
            y=yy,
            z=zz,
            colorscale=[[0, body_color], [1, body_color]],
            cauto=False,
            cmin=0,
            cmax=1,
            showlegend=True,
            showscale=False,
            name=body.name,
        )
        figure.add_trace(spheres[body.name])

        labels[body.name] = go.Scatter3d(
            x=[body.r[0].x.value],
            y=[body.r[0].x.value],
            z=[body.r[0].x.value],
            mode='text',
            text=body.name,
            showlegend=False
        )
        figure.add_trace(labels[body.name])
    
    def fn(t, bodies=list(args.bodies), **kwargs):
        for body in bodies:
            xx, yy, zz = axtools.create_sphere(body.r[t.value], body.radius)
            spheres[body.name].update(x=xx, y=yy, z=zz)

            labels[body.name].update(
                x=[body.r[t.value].x.value],
                y=[body.r[t.value].y.value],
                z=[body.r[t.value].z.value]
            )

            trails[body.name]['x'].append(body.r[t.value].x.value)
            trails[body.name]['y'].append(body.r[t.value].y.value)
            trails[body.name]['z'].append(body.r[t.value].z.value)
            
            trail_trace = go.Scatter3d(
                x=trails[body.name]['x'],
                y=trails[body.name]['y'],
                z=trails[body.name]['z'],
                mode='lines',
                line=dict(color=body_color),
                showlegend=False
            )
            figure.add_trace(trail_trace)
        figure.update_traces()
        print(f"Timestep {t} ({((t / args.limit) * 100).value:.2f}% complete)", end="\r")
    
    f2.show()
    return fn