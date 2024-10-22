from sympy.abc import x
from sympy import solve
def e(x: int, y: int): return x * (10 ** y)

def conversions(scale):
    def fn(self, other, _type):
        if _type == 'add': return type(self)((self.value * scale) + other.value)
        elif _type == 'sub': return type(self)((self.value * scale) - other.value)
        elif _type == 'mul': return type(self)((self.value * scale) * other.value)
        elif _type == 'div': return type(self)((self.value * scale) / other.value)
    return fn