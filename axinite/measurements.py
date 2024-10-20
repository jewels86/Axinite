from axinite.functions import e

class Measurement:
    def __init__(self, value: int):
        self.value = value
        self.conversions = {}
    def __add__(self, other):
        if type(other) not in self.conversions: return self.value + other.value
        return self.conversions[type(other)](self, other, 'add') 
    def __sub__(self, other):
        if type(other) not in self.conversions: return self.value - other.value
        return self.conversions[type(other)](self, other, 'sub') 
    def __mul__(self, other):
        if type(other) not in self.conversions: return self.value * other.value
        return self.conversions[type(other)](self, other, 'mul')
    def __div__(self, other):
        if type(other) not in self.conversions: return self.value / other.value
        return self.conversions[type(other)](self, other, 'div') 
    
    def __str__(self): return f"{self.value} {type(self)}"
    def __repr__(self): return self.__str__()
    def __eq__(self, other): 
        if type(other) not in self.conversions: raise Exception(f"{self} cannot be converted to {other}.")
        return type(other)(self.conversions[type(other)]).value == self.value 
    
class Volume(Measurement):
    def __init__(self, value: int): super(Volume, self).__init__(value)
class Area(Measurement):
    def __init__(self, value: int): super(Area, self).__init__(value)
class Mass(Measurement):
    def __init__(self, value: int): super(Mass, self).__init__(value)
class Distance(Measurement):
    def __init__(self, value: int): super(Distance, self).__init__(value)
class Temperature(Measurement):
    def __init__(self, value: int): super(Temperature, self).__init__(value)
class Force(Measurement):
    def __init__(self, value: int): super(Force, self).__init__(value)
class Velocity(Measurement):
    def __init__(self, value: int): super(Velocity, self).__init__(value)
class Time(Measurement):
    def __init__(self, value: int): super(Time, self).__init__(value)

class Km3(Volume):
    def __init__(self, value: int = 0): 
        super(Km3, self).__init__(value)
        self.conversions = {
            Km3: self.toKm3, 
            m3: self.toMeter3
        }
        
    def toMeter3(self): return m3(e(self.value, 3))
    def toKm3(self): return self.value
    
class Km2(Area):
    def __init__(self, value: int = 0): super(Km2, self).__init__(value)
    
class Kg(Mass):
    def __init__(self, value: int = 0): super(Kg, self).__init__(value)
    
class Km(Distance):
    def __init__(self, value: int = 0): super(Km, self).__init__(value)

class m(Distance):
    def __init__(self, value: int = 0): super(m, self).__init__(value)
    
class Celsius(Temperature):
    def __init__(self, value: int = 0): super(Celsius, self).__init__(value)
    
class N(Temperature):
    def __init__(self, value: int = 0): super(N, self).__init__(value)
    
class Degrees(Measurement):
    def __init__(self, value: int = 0): super(Degrees, self).__init__(value)
    
class mPers(Velocity):
    def __init__(self, value: int = 0): super(mPers, self).__init__(value)

class s(Time):
    def __init__(self, value: int = 0): super(s, self).__init__(value)

class m3(Volume):
    def __init__(self, value: int = 0): super(m3, self).__init__(value)