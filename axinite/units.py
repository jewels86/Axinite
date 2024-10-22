from axinite.functions import e, conversions

class Unit:
    def __init__(self, value: int, label: str):
        self.value = value
        self.label = label
        self.conversions = {}
    def __add__(self, other):
        if type(other) not in self.conversions: return self.value + other.value
        return self.conversions[type(other)](other, 'add') 
    def __sub__(self, other):
        if type(other) not in self.conversions: return self.value - other.value
        return self.conversions[type(other)](other, 'sub') 
    def __mul__(self, other):
        if type(other) not in self.conversions: return self.value * other.value
        return self.conversions[type(other)](other, 'mul')
    def __truediv__(self, other):
        if type(other) not in self.conversions: return self.value / other.value
        return self.conversions[type(other)](other, 'div') 
    
    def __str__(self): return f"{self.value} {self.label}"
    def __repr__(self): return self.__str__()
    def __eq__(self, other): 
        if type(other) not in self.conversions: raise Exception(f"{self} cannot be converted to {other}.")
        return type(other)(self.conversions[type(other)]).value == self.value 
    
class Volume(Unit):
    def __init__(self, value: int, label: str): super(Volume, self).__init__(value, label)
class Area(Unit):
    def __init__(self, value: int, label: str): super(Area, self).__init__(value, label)
class Mass(Unit):
    def __init__(self, value: int, label: str): super(Mass, self).__init__(value, label)
class Distance(Unit):
    def __init__(self, value: int, label: str): super(Distance, self).__init__(value, label)
class Temperature(Unit):
    def __init__(self, value: int, label: str): super(Temperature, self).__init__(value, label)
class Force(Unit):
    def __init__(self, value: int, label: str): super(Force, self).__init__(value, label)
class Velocity(Unit):
    def __init__(self, value: int, label: str): super(Velocity, self).__init__(value, label)
class Time(Unit):
    def __init__(self, value: int, label: str): super(Time, self).__init__(value, label)

class Km3(Volume):
    def __init__(self, value: int = 0): 
        super(Km3, self).__init__(value, "Km^3")
        self.conversions = {
            Km3: conversions(1), 
            m3: conversions(e(1, 3)),
            s: self.s
        }
    
    def s(self, other, type):
        if type == 'div': return m3Ps(e(self.value, 3) / other.value)
        else: raise Exception()
    
class Km2(Area):
    def __init__(self, value: int = 0): super(Km2, self).__init__(value, "Km^2")
    
class Kg(Mass):
    def __init__(self, value: int = 0): super(Kg, self).__init__(value, "Kg")
    
class Km(Distance):
    def __init__(self, value: int = 0): super(Km, self).__init__(value, "Km")

class m(Distance):
    def __init__(self, value: int = 0): super(m, self).__init__(value, "m")
    
class Celsius(Temperature):
    def __init__(self, value: int = 0): super(Celsius, self).__init__(value, "C°")
    
class N(Temperature):
    def __init__(self, value: int = 0): super(N, self).__init__(value, "N")
    
class Degrees(Unit):
    def __init__(self, value: int = 0): super(Degrees, self).__init__(value, "°")
    
class mPs(Velocity):
    def __init__(self, value: int = 0): super(mPs, self).__init__(value, "m/s")

class s(Time):
    def __init__(self, value: int = 0): super(s, self).__init__(value, "s")

class m3(Volume):
    def __init__(self, value: int = 0): super(m3, self).__init__(value, "m^3")
    
class m3Ps(Velocity):
    def __init__(self, value: int = 0): super(m3Ps, self).__init__(value, "m^3/s")