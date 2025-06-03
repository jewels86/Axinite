from axinite import axtools, ax, axana
import logging, sys
from numba import njit

path = "inner-solar-system.tmpl.ax"
t_start = ax.interpret_time("686d * 60") # 60 martian orbital periods in, start looking
t_end = ax.interpret_time("686d * 100") # 100 martian orbital periods in, stop
backend = ax.verlet_backend

source = "Earth"
dest = "Mars"

max_thrust = 0.9e6 # in newtons, fill in yourself
mass_initial = 1e5
@njit
def mass(t): return mass_initial # again, fill in yourself- mass over time

logger = logging.getLogger('rocket-logger')
logger.info(f"Logger started with t_start of {t_start} and {t_end}, whatever those mean")

try:
    args = axtools.read(path)
    args.limit = t_end
    args.backend = backend
    axtools.load(args, verbose=True)
    
    
    for body in args.bodies:
        if body.name == source: source_body = body
        if body.name == dest: dest_body = body
    
    logger.info(f"Finished! {args.limit/args.delta} timesteps computed.")
    logger.info(f"Creating equations of motion to calculate interceptions...")

    inner_source = source_body.inner
    inner_dest = dest_body.inner

    def v_source(t):
        return inner_source.vs[t]

except Exception as e:
    logger.error(f"Could not read from {path}, got error: {e}")
    logger.info(f"Make sure you download the requiredfils first- 'axcli catalog' can help")
    sys.exit(-1)