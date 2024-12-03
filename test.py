import axinite as ax
import lite as lt

args = lt.read("templates/tri-body.tmpl.ax")
bodies = lt.load(args, "tri-body.ax")
lt.show(*bodies)