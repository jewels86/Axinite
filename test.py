import axinite as ax
import axtools as axt
import astropy.units as u

#args = lt.read("templates/solar-system.tmpl.ax")
#t, bodies = lt.load(args, "solar-system.ax")
args = axt.read("tri-body.ax")
axt.show(args.t.value, args.delta.value, *args.bodies, radius_multiplier=args.radius_multiplier, speed=args.rate, retain=args.retain)