import axinite as ax
import axinite.tools as axtools
import axinite.analysis as axana

args = axtools.read("examples/solar-system/my-solar-system.tmpl.ax")
bodies = axtools.load(args, verbose=True)

longest = 0

for body in bodies[1:]:
    orbit = axana.Orbit(bodies[0], body)
    print(f"{body.name}: {orbit.orbital_period}")
    if orbit.orbital_period > longest:
        longest = orbit.orbital_period

print(f"The longest orbital period is {longest} seconds, or:")
print(f"{ax.time_to(longest, "min", round_digits=2)},")
print(f"{ax.time_to(longest, "hr", round_digits=2)},")
print(f"{ax.time_to(longest, "d", round_digits=2)},")
print(f"{ax.time_to(longest, "yr", round_digits=2)}")