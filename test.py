import axinite as ax
import axtools as axt
import astropy.units as u

args = axt.read("templates/solar-system.tmpl.ax")
bodies = axt.load(args, "solar-system.ax")
args = axt.read("solar-system.ax")
axt.show(args.t.value, args.delta.value, *args.bodies, radius_multiplier=args.radius_multiplier, retain=args.retain)