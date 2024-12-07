import axinite as ax
import lite as lt
import astropy.units as u

#args = lt.read("templates/solar-system.tmpl.ax")
#t, bodies = lt.load(args, "solar-system.ax")
args = lt.read("solar-system.ax")
lt.show(args.t.value, args.delta.value, *args.bodies, radius_multiplier=args.radius_multiplier)