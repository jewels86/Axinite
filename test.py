from axinite import Body, Vector3, Km3, Kg, e, formulas, CompoundM, units, CompoundD, m, s
from trimesh import Trimesh

#primary = Body("primary", Trimesh(), Vector3(0, 0, 0), Km3(e(1.083, 12)), Kg(e(5.97, 24)))
#secondary = Body("secondary", Trimesh(), Vector3(1, 1, 1), Km3(e(1.083, 12)), Kg(e(5.97, 24)))

first = CompoundD(m(2), s(1))
second = CompoundD(m(32), s(4))

print(first.above, first.below, first)
print(second.above, second.below, second)

print("+", first + second, second + first)
print("-", first - second, second - first)
print("*", first * second, second * first)
print("/", first / second, second / first)