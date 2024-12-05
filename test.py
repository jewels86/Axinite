import axinite as ax
import lite as lt
import astropy.units as u

#args = lt.read("templates/tri-body.tmpl.ax")
#t, bodies = lt.load(args, "tri-body.ax")
args = lt.read("tri-body.ax")
lt.show(args.t, args.delta, *args.bodies)
