from astropy import units as u
from axinite import Body
from trimesh import Trimesh
import axinite
import axinite.shapes

Body(axinite.shapes.create_cube(1.), 1.0 * u.meter)

axinite.shapes.create_sphere().show()