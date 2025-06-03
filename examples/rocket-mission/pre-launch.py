from axinite import axtools, ax, axana
import logging, sys
from numba import njit
import numpy as np

path = "inner-solar-system.tmpl.ax"
t_start = ax.interpret_time("686d") * 60
t_end = ax.interpret_time("686d") * 60
backend = ax.verlet_backend

source = "Earth"
dest = "Mars"

max_thrust = 0.9e6  # N
mass_initial = 1e5  # kg
Isp = 300  # seconds
g0 = 9.80665

@njit
def mass(t):
    return mass_initial - (t * max_thrust / (Isp * g0))  # classic rocket equation approximation

logger = logging.getLogger('rocket-logger')
logging.basicConfig(level=logging.INFO)
logger.info(f"Logger started with t_start of {t_start} and {t_end}, whatever those mean")

try:
    args = axtools.read(path)
    args.limit = t_end
    args.backend = backend
    axtools.load(args, verbose=True)

    def get_body(name):
        for body in args.bodies:
            if body.name == name:
                return body
        raise ValueError(f"Body '{name}' not found.")

    source_body = get_body(source)
    dest_body = get_body(dest)

    logger.info(f"Finished! {args.limit/args.delta} timesteps computed.")
    logger.info(f"Setting up simulation...")

    r_source = lambda n: source_body._inner["r"][n]
    v_source = lambda n: source_body._inner["v"][n]
    r_dest = lambda n: dest_body._inner["r"][n]
    v_dest = lambda n: dest_body._inner["v"][n]
    d = args.delta  # time step

    t_start = ax.round_limit(t_start, d)
    t_end = ax.round_limit(t_end, d)

    def compute_gravity(n, r):
        F_total = np.zeros(3)
        for body in args.bodies:
            r_body = body._inner["r"][n]
            F_total += ax.gravitational_force_jit(
                body._inner["m"], mass(n * d), r_body - r
            )
        return F_total

    def thrust_toward_target(n, r):
        direction = r_dest(n) - r
        unit = direction / np.linalg.norm(direction)
        return max_thrust * unit

    def simulate_rocket(n_start, n_end):
        r = np.copy(r_source(n_start))
        v = np.copy(v_source(n_start))
        traj = [r.copy()]
        for n in range(n_start, n_end):
            F_g = compute_gravity(n, r)
            F_t = thrust_toward_target(n, r)
            a = (F_g + F_t) / mass(n * d)
            v += a * d
            r += v * d
            traj.append(r.copy())

            # Intercept detection (optional)
            dist = np.linalg.norm(r - r_dest(n))
            if dist < 1e6:
                logger.info(f"Close approach at step {n}, distance: {dist}")
                break

        return traj

    # Example run
    start_index = int(t_start / d)
    end_index = int(t_end / d)
    logger.info("Simulating trajectory...")
    trajectory = simulate_rocket(start_index, end_index)

    logger.info("Simulation complete.")


except Exception as e:
    logger.error(f"Could not read from {path}, got error: {e}")
    logger.info(f"Make sure you download the required files first- 'axcli catalog' can help")
    sys.exit(-1)