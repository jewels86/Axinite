from astropy.coordinates import CartesianRepresentation
from astropy.units import Quantity
import math

def apply_to_vector(vector: CartesianRepresentation, function):
    return CartesianRepresentation([function(i) for i in vector.xyz])

def vector_to(vector: CartesianRepresentation, unit: Quantity):
    return apply_to_vector(vector, lambda i: i.to(unit))

def vector_magnitude(vector: CartesianRepresentation):
    return math.sqrt(vector.x.value**2 + vector.y.value**2 + vector.z.value**2) * vector.x.unit