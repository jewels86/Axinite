from axinite.measurements import Mass, Distance, N, Kg, m, mPers
import math

G = 6.6743 * (10 ** -11)

def gravity_from_mass(m1: Kg, m2: Kg, r: m):
    return N(G * ((m1 * m2).value / (r ** 2).value))
def escape_velocity(mass: Kg, r: m):
    return mPers(math.sqrt((2 * G * mass.value) / r.value))