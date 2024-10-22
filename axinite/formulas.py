from axinite.units import Mass, Distance, N, Kg, m, mPs, Km
import math

G = 6.6743 * (10 ** -11)

def gravity_from_mass(m1: Kg, m2: Kg, r: m):
    return N(G * ((m1 * m2) / (r ** 2)))
def escape_velocity(mass: Kg, r: m):
    return mPs(math.sqrt((2 * G * mass.value) / r.value))
def gravitational_acceleration(m: Kg, r: m):
    return (G * m.value) / (r.value ** 2)