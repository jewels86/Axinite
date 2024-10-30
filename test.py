import axinite

cmpdA1 = axinite.CompoundA(axinite.m(1), axinite.m(2), axinite.m(3))
cmpdA2 = axinite.CompoundA(axinite.km(1))

print(cmpdA1)
print(cmpdA2)
print(cmpdA1 + cmpdA2)
print(axinite.m(1) + axinite.km(1))
