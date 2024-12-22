import axinite.tools as axtools
import plotly.graph_objects as go
from itertools import cycle
import os, signal

def plotly_frontend(args: axtools.AxiniteArgs, mode: str, theme="plotly_dark", use_min=True):
    if mode != "show": raise Exception("plotly_frontend is only supported in show mode.")
    if args.rate is None:
        args.rate = 100
    if args.radius_multiplier is None:
        args.radius_multiplier = 1
    if args.retain is None:
       args.retain = 200
    if args.frontend_args != {} and "plotly" in args.frontend_args:
        if "theme" in args.frontend_args["plotly"]:
            theme = args.frontend_args["plotly"]["theme"]
        if "use_min" in args.frontend_args["plotly"]:
            use_min = args.frontend_args["plotly"]["use_min"]

    minlen = axtools.min_axis_length(*args.bodies, radius_multiplier=args.radius_multiplier)
    maxlen = axtools.max_axis_length(*args.bodies, radius_multiplier=args.radius_multiplier)

    range = [minlen if use_min else -maxlen, maxlen]

    colors = cycle(['red', 'blue', 'green', 'orange', 'purple', 'yellow'])

    fig = go.Figure()
    layout = go.Layout(
        autosize=True,
        template=theme,
        scene=dict(
            aspectmode='cube',
            xaxis=dict(range=range),
            yaxis=dict(range=range),
            zaxis=dict(range=range)
        )
    )
    fig.update_layout(layout)

    def fn(body: axtools.Body):
        body_color = body.color if body.color != "" else next(colors)
        xx, yy, zz = axtools.create_sphere(body.r[0], body.radius * body.radius_multiplier)
        fig.add_trace(go.Surface(
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
            opacity=0.2
        ))
        fig.add_trace(go.Scatter3d(
            x=[body.r[0].x.value],
            y=[body.r[0].y.value],
            z=[body.r[0].z.value],
            mode='text',
            text=[body.name],
            textposition='top center',
            showlegend=False
        ))
        trajectory_x = [point.x.value for point in body.r.values()]
        trajectory_y = [point.y.value for point in body.r.values()]
        trajectory_z = [point.z.value for point in body.r.values()]
        fig.add_trace(go.Scatter3d(
            x=trajectory_x,
            y=trajectory_y,
            z=trajectory_z,
            mode='lines',
            line=dict(color=body_color, width=2),
            name=f"{body.name} trajectory",
            showlegend=False
        ))

        
    return fn, fig.show, lambda: os.kill(os.getpid(), signal.SIGINT)