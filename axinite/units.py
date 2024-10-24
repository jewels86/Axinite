from axinite.functions import e, conversions, conversions_distance

class Unit:
    def __init__(self, value: int, negative=False):
        self.value = value
        self.conversions = {}
        self.scales = {}
        self.exponential_units = {}
        self.negative = negative
        self.exponent = 1
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
    def __neg__(self):
        return type(self)(value=-self.value, negative=True)
    
    def to(self, type):
        return type(self.scales[type] * self.value)
    
    def __str__(self, novalue=False): return f"{self.value if novalue == False else ""}{self.label}{f"^{self.exponent}" if self.exponent != 1 else ""}"
    def __repr__(self): return self.__str__()
    def __eq__(self, other): 
        if type(other) not in self.conversions: raise Exception(f"{self} cannot be converted to {other}.")
        return type(other)(self.conversions[type(other)]).value == self.value
    
class CompoundM(Unit):
    def __init__(self, *values, value=None):
        super(CompoundM, self).__init__(1)
        if not hasattr(self, 'label'): 
            self._isclass = False
            self.label = ""
        else: self._isclass = True
        
        self.units_t = []
        self.units_t_v = []
        self.units_v = []
        for v in values: 
            self.units_t.append(type(v))
            self.units_v.append(v)
            self.value *= v.value
            self.label += f" {v.label}"
        if value != None: self.value = value
        self.simplify()
        
    def simplify(self):
        refn = {}
        refv = {}
        
        for u in self.units_v:
            if type(u) not in refn: 
                refn[type(u)] = 0
                refv[type(u)] = []
            if u.negative == False: refn[type(u)] += 1
            else: refn[type(u)] -= 1
            refv[type(u)].append(u)

        _units_t = []
        v = 1
        
        for k, v in refn.items():
            try: 
                t = k(0).exponential_units[v]
                _units_t.append(t)
                self.units_t_v.append(t(0))
            except: 
                t = k(0)
                t.exponent = v
                _units_t.append(type(t))
                self.units_t_v.append(t)
            
            
        self.units_t = _units_t
        self.label = ""
        
        for item in self.units_t_v:
            if not self._isclass: self.label = ''.join([self.label, f" {item.__str__(novalue=True)}"])
        
    def __add__(self, other):
        if type(other) != CompoundM or self.units_t != other.units_t: raise Exception()
        return CompoundM(*self.units_v, value = self.value + other.value)
    def __sub__(self, other):
        if type(other) != CompoundM or self.units_t != other.units_t: raise Exception()
        return CompoundM(*self.units_v, value = self.value - other.value)
    def __mul__(self, other):
        if type(other) == CompoundM: return CompoundM(*(self.units_v + other.units_v), value=self.value * other.value)
        return CompoundM(self.units_v + [other], value = self.value * other.value)
    def __truediv__(self, other):
        if type(other) == CompoundM: return CompoundM(*(self.units_v + [-u for u in other.units_v]), value=self.value / other.value)
        return CompoundM(self.units_v + [-other], value = self.value / other.value)
    def __neg__(self):
        return type(self)(*self.units_v, value=-self.value)
    
    def __contains__(self, type):
        for t in self.units_t:
            if t == type: return True
        return False
    
class CompoundD(Unit):
    def __init__(self, above: Unit, below: Unit):
        super(CompoundD, self).__init__(above.value / below.value, f"{above.label} /{below.label} ")
        if not hasattr(self, 'label'):
            self._isclass = True
            self.label = ""
        else: self._isclass = True
        
        self.above = above
        self.below = below
    
    def __eq__(self, other):
        if self.above != other.above: return False
        if self.below != other.below: return False
        if self.value != other.value: return False
        return True
    
    def __add__(self, other):
        if type(self.above) != type(other.above): raise Exception()
        if type(self.below) != type(other.below): raise Exception()
        return CompoundD(self.above + other.above, type(self.below)(value=0))
    
class Volume(CompoundM):
    def __init__(self, unit1: Unit, unit2: Unit, unit3: Unit, value: int = None, negative: bool = False): super(Volume, self).__init__(unit1, unit2, unit3, value=value)
class Area(Unit):
    def __init__(self, value: int): super(Area, self).__init__(value)
class Hypervolume(CompoundM):
    def __init__(self, unit1: Unit, unit2: Unit, unit3: Unit, unit4: Unit, value: int = None, negative: bool = False): super(Hypervolume, self).__init__(unit1, unit2, unit3, unit4, value=value)
class Mass(Unit):
    def __init__(self, value: int, negative: bool = False): super(Mass, self).__init__(value, negative=negative)
class Distance(Unit):
    def __init__(self, value: int, negative: bool = False): super(Distance, self).__init__(value, negative=negative)
class Temperature(Unit):
    def __init__(self, value: int, negative: bool = False): super(Temperature, self).__init__(value, negative=negative)
class Force(Unit):
    def __init__(self, value: int, negative: bool = False): super(Force, self).__init__(value, negative=negative)
class Velocity(Unit):
    def __init__(self, value: int, negative: bool = False): super(Velocity, self).__init__(value, negative=negative)
class Time(Unit):
    def __init__(self, value: int, negative: bool = False): super(Time, self).__init__(value, negative=negative)

class Km3(Volume):
    label = "Km^3"
    def __init__(self, value: int = 0, negative=False): 
        super(Km3, self).__init__(m(), m(), m(), value = value, negative=negative)
        self.conversions = {
            Km3: conversions(self, 1), 
            m3: conversions(self, e(1, -3)),
            s: self.s
        }
    
    def s(self, other, type):
        if type == 'div': return m3Ps(e(self.value, 3) / other.value)
        else: raise Exception()
    
class Km2(Area):
    label = "Km^2"
    def __init__(self, value: int = 0, negative=False): super(Km2, self).__init__(value, negative=negative)
    
class Kg(Mass):
    label = "Kg"
    def __init__(self, value: int = 0, negative=False): 
        super(Kg, self).__init__(value, negative=negative)
        self.scales = {
            Kg: 1
        }
    
class Km(Distance):
    label = "Km"
    def __init__(self, value: int = 0, negative=False): 
        super(Km, self).__init__(value, negative=negative)
        self.conversions = {
            Km: conversions_distance(self, 1, Km2),
            m: conversions_distance(self, e(1, -3), m2)
        }

class m(Distance):
    label = "m"
    def __init__(self, value: int = 0, negative=False): 
        super(m, self).__init__(value, negative=negative)
        self.conversions = {
            m: conversions_distance(self, 1, m2),
            Km: conversions_distance(self, 0.001, Km2)
        }
        self.exponential_units = {
            1: m, 2: m2, 3: m3, 4: m4
        }
    
class Celsius(Temperature):
    label = "C°"
    def __init__(self, value: int = 0, negative=False): super(Celsius, self).__init__(value, negative=negative)
    
class N(Temperature):
    label = "N"
    def __init__(self, value: int = 0, negative=False): super(N, self).__init__(value, negative=negative)
    
class Degrees(Unit):
    label = "°"
    def __init__(self, value: int = 0, negative=False): super(Degrees, self).__init__(value, negative=negative)
    
class mPs(Velocity):
    label = "m/s"
    def __init__(self, value: int = 0, negative=False): super(mPs, self).__init__(value, negative=negative)

class s(Time):
    label = "s"
    def __init__(self, value: int = 0, negative=False): 
        super(s, self).__init__(value, negative=negative)
        self.conversions = {
            s: conversions(self, 1),
            min: conversions(self, 60)
        }

class m3(Volume):
    label = "m^3"
    def __init__(self, unit1, unit2, unit3, value: int = None, negative=False): super(m3, self).__init__(unit1, unit2, unit3, value = value, negative=negative)

class m4(Hypervolume):
    label = "m^4"
    def __init__(self, unit1, unit2, unit3, unit4, value: int = None, negative=False): super(m3, self).__init__(unit1, unit2, unit3, unit4, value = value, negative=negative)
    
class m2(Area):
    label = "m^2"
    def __init__(self, value: int = 0, negative=False): super(m2, self).__init__(value, negative=negative)
    
class m3Ps(Velocity):
    label = "m^3/s"
    def __init__(self, value: int = 0, negative=False): super(m3Ps, self).__init__(value, negative=negative)

class min(Time):
    label = "min"
    def __init__(self, value: int = 0, negative=False): 
        super(min, self).__init__(value, negative=negative)
        self.conversions = {
            s: conversions(self, (1 / 60)),
            min: conversions(self, 1)
        }