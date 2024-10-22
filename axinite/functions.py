from sympy.abc import x
from sympy import solve
def e(x: int, y: int): return x * (10 ** y)

def conversions(self, scale):
    def fn(other, _type):
        if _type == 'add': return type(self)(self.value + (other.value * scale))
        if _type == 'sub': return type(self)(self.value - (other.value * scale))
        if _type == 'mul': return type(self)(self.value * (other.value * scale))
        if _type == 'div': return type(self)(self.value / (other.value * scale))
    return fn

def conversions_distance(self, scale, squared):
    def fn(other, _type):
        if _type == 'mul': return squared((other.value * scale) * self.value)
        else: return conversions(self, scale)(other, _type)
    return fn