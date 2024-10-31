import axinite

cmpdA1 = axinite.CompoundA(axinite.m(1), axinite.m(2), axinite.m(3))
cmpdA2 = axinite.CompoundA(axinite.km(1))
cmpdS1 = axinite.CompoundS(axinite.m(1), axinite.m(2), axinite.m(3))
cmpdS2 = axinite.CompoundS(axinite.km(1))

print(cmpdS1)
print(cmpdS2)
print(cmpdS1 + cmpdS2)
print(cmpdS1 + cmpdA1)