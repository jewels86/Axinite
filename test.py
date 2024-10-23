from axinite import Body, Vector3, Km3, Kg, e, formulas, CompoundM, units, CompoundD
from trimesh import Trimesh

#primary = Body("primary", Trimesh(), Vector3(0, 0, 0), Km3(e(1.083, 12)), Kg(e(5.97, 24)))
#secondary = Body("secondary", Trimesh(), Vector3(1, 1, 1), Km3(e(1.083, 12)), Kg(e(5.97, 24)))

first = CompoundM(units.m(2), units.Km(2), units.s(30))
second = CompoundM(units.m2(82), units.m(0.5))
third = CompoundD(units.m(40), units.Km(4))
fourth = CompoundD(first, second)

print(first)
print(second)
print(third)
print(fourth)