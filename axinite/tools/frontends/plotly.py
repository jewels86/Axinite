import axinite.tools as axtools
import plotly.graph_objects as go
from itertools import cycle

def plotly_frontend(args: axtools.AxiniteArgs, mode: str, theme="plotly_dark"):
    if mode != "show": raise Exception("plotly_frontend is only supported in show mode.")

    maxlen = axtools.max_axis_length(*args.bodies, radius_multiplier=args.radius_multiplier)

    colors = cycle(['red', 'blue', 'green', 'orange', 'purple', 'yellow'])

    fig = go.Figure()
    layout = go.Layout(
        title=args.name,
        autosize=False,
        template=theme,
        scene=dict(
            xaxis=dict(range=[-maxlen, maxlen]),
            yaxis=dict(range=[-maxlen, maxlen]),
            zaxis=dict(range=[-maxlen, maxlen])
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
    
    return fn