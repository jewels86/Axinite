from axinite import axtools, ax, axana
import logging, sys
from numba import njit
import numpy as np

path = "inner-solar-system.tmpl.ax"
t_start = ax.interpret_time("686d") * 60
t_end = ax.interpret_time("686d") * 100
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
logger.info(f"Logger started with t_start of {t_start} and {t_end}, whatever those mean (they are in seconds).")

try:
    if path.endswith(".tmpl.ax"):
        logger.info(f"Loading template file {path}...")
        args = axtools.read(path)
        args.set_limit(t_end)
        args.backend = backend

        logger.info(f"Loading bodies from {path} with limit {args.limit} (from {t_end} - may have been rounded)...")

        axtools.load(args, verbose=True)
        axtools.save(args, path.replace(".tmpl.ax", ".ax"))
        logger.info(f"Template file loaded and saved as {path.replace('.tmpl.ax', '.ax')}.")
    else:
        logger.info(f"Loading file {path}...")
        args = axtools.read(path)
        args.set_limit(t_end)
        args.backend = backend

    def get_body(name):
        for body in args.bodies:
            if body.name == name:
                return body
        raise ValueError(f"Body '{name}' not found.")

    source_body = get_body(source)
    dest_body = get_body(dest)

    logger.info(f"Finished! {args.limit/args.delta} timesteps computed.")
    logger.info(f"Setting up simulation...")

    _r_source = source_body._inner["r"]
    _v_source = source_body._inner["v"]
    _r_dest = dest_body._inner["r"]
    _v_dest = dest_body._inner["v"]
    r_source = njit(lambda n: _r_source[n])
    v_source = njit(lambda n: _v_source[n])
    r_dest = njit(lambda n: _r_dest[n])
    v_dest = njit(lambda n: _v_dest[n])
    d = args.delta 

    t_start = ax.round_limit(t_start, d)
    t_end = ax.round_limit(t_end, d)
    inners = [body._inner for body in args.bodies]

    @njit
    def compute_gravity(n, r, inners):
        F_total = np.zeros(3)
        for body in inners:
            r_body = body["r"][n]
            F_total += ax.gravitational_force_jit(
                body["m"], mass(n * d), r_body - r
            )
        return F_total

    @njit
    def thrust_toward_target(n, r):
        direction = r_dest(n) - r
        unit = direction / np.linalg.norm(direction)
        return max_thrust * unit

    @njit
    def simulate_rocket(n_start, n_end, inners):
        r = np.copy(r_source(n_start))
        v = np.copy(v_source(n_start))
        traj = [r.copy()]
        for n in range(n_start, n_end):
            F_g = compute_gravity(n, r, inners)
            F_t = thrust_toward_target(n, r)
            a = (F_g + F_t) / mass(n * d)
            v += a * d
            r += v * d
            traj.append(r.copy())

            dist = np.linalg.norm(r - r_dest(n))
            if dist < 1e6:
                print("Intercept detected! Following data is in (seconds, n)", n*d, n)
                break

        return traj

    start_index = int(ax.round_limit(t_start, d) / d)
    end_index = int(ax.round_limit(t_end, d) / d)
    logger.info(f"Simulating trajectory from {start_index}n to {end_index}n...")
    trajectory = simulate_rocket(start_index, end_index - 1, inners)

    logger.info("Simulation complete.")


except Exception as e:
    logger.error(f"Could not read from {path}, got error: {e}")
    logger.info(f"Make sure you download the required files first- 'axcli catalog' can help")
    # raise e
    sys.exit(-1)