import axinite.tools as axtools
import matplotlib.pyplot as ply

def mpl_frontend(args: axtools.Body, mode: str):
    if mode != "show": raise Exception("mpl_frontend is only supported in show mode")
