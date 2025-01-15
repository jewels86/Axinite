import axinite as ax
import axinite.tools as axtools
import axinite.analysis as axana

args = axtools.read("rocket-launch.tmpl.ax")
bodies = axtools.load(args, verbose=True)

result = axana.intercept(bodies[3], bodies[2], (0, 1.1e4), ax.timesteps(args.limit, args.delta), args.delta, True)

print(f"Speed: {result[0]} m/s")
print(f"Position: {result[1]} m")
print(f"Time: {result[2]} n")
print(f"Unit Vector: {result[3].tolist()}")