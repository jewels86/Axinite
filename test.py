import axinite as ax
from astropy import units as u
from astropy import constants as const
from astropy.coordinates import CartesianRepresentation

A = ax.Body(
    "A", 
    const.M_earth.to(u.kg), 
    CartesianRepresentation([0, 0, 0] * u.kilometer), 
    CartesianRepresentation([0, 0, 0] * u.kilometer / u.second),
    const.R_earth.to(u.kilometer)
)
B = ax.Body(
    "B",
    7.342e22 * u.kg,
    CartesianRepresentation([405500, 0, 0] * u.kilometer),
    CartesianRepresentation([0, 0, 0] * u.kilometer / u.second),
    1737.4 * u.kilometer
)

t = 0
delta_t = 0.5 * u.second
dt_val = 0.5

rB = {
    0: B.position
}
vB = {
    0: B.velocity
}
aB = {
    0: A.gravitational_force(B)
}

try:
    for i in range(0, 120):
        aB[t + dt_val] = A.gravitational_force(B)
        rB[t + 0.5] = (rB[t]) + (vB[t] * 0.5) + (0.5 * aB[t] * delta_t**2)
        print(0.5 * (aB[t] + aB[t + 0.5]), vB[t], delta_t)
        vB[t + 0.5] = vB[t] + ((0.5 * (aB[t] + aB[t + 0.5])) * delta_t)
        t += 0.5
except Exception as e:
    print(e)
print(rB)
print(vB)