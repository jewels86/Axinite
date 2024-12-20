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
    
    figure = go.Figure()
    layout = go.Layout()
    figure.update_layout(layout)
    
    