import axinite as ax
import axinite.tools as axtools
import axinite.analysis as axana

args = axtools.read("rocket-launch.tmpl.ax")
bodies = axtools.load(args)

result = axana.intercept(bodies[4], bodies[3], (7e3, 1.1e4), ax.timesteps(args.limit, args.delta), 5000, verbose=True)

print(f"Speed: {result[0]} m/s")
print(f"Position: {result[1]} m")
print(f"Time: {result[2]} n")