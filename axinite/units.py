from axinite.functions import *

class Unit:
    example = lambda x: Unit(x)
    
    def __init__(self, value):
        self.value = value
        
    def __add__(self, other):
        if type(other) in self.conversions: 
            return type(self).example(other.conversions[type(self)](other.value) + self.value)
        return CompoundA(self, other)
    
    def __neg__(self):
        return type(self).example(-self.value)
        
    def __str__(self):
        return f'{self.value}{self.label}'
    def __repr__(self): return str(self)
        
class Compound(Unit):
    def __init__(self, value, *values):
        super().__init__(value)
        self.values = list(values)

class CompoundA(Compound):
    example = lambda x: CompoundA(*[Unit(x)])
    
    def __init__(self, *values):
        val = 0
        simplified_v = {}
        simplified = []
        for v in values: 
            val += v.value
            try: simplified_v[type(v)].append(v.value)
            except: simplified_v[type(v)] = [v.value]

        for k, v in simplified_v.items():
            if k is Compound: 
                print('was compound')
                [simplified.append(_v) for _v in v]
                continue
            total_value = 0
            for _v in v:
                total_value += _v
            simplified.append(k.example(total_value))
        
        super().__init__(val, *values)
        self.simplified = simplified
        self.label = ''
    
    def __add__(self, other):
        if isinstance(other, Compound): return CompoundA(*(self.values + other.values))
        return CompoundA(*(self.values + [other]))
    
    def __str__(self):
        return '+'.join(f'{val}' for val in self.simplified)
    def __repr__(self): return str(self)

class CompoundS(Compound):
    def __init__(self, *values):
        val = 0
        simplified_v = {}
        simplified = []
        for v in values: 
            val -= v.value
            try: simplified_v[type(v)].append(v.value)
            except: simplified_v[type(v)] = [v.value]

        for k, v in simplified_v.items():
            if k is Compound: 
                print('was compound')
                [simplified.append(_v) for _v in v]
                continue
            total_value = 0
            for _v in v:
                total_value -= _v
            simplified.append(k.example(total_value))
        
        super().__init__(val, *values)
        self.simplified = simplified
        self.label = ''
    
    def __add__(self, other):
        if isinstance(other, CompoundS): return CompoundS(*(self.values + other.values))
        return CompoundA(self, other)
    def __sub__(self, other):
        if isinstance(other, Compound): return CompoundS(*(self.values + other.values))
        return CompoundS(*(self.values + [other]))
    
    def __str__(self):
        return '-'.join(f'{val}' for val in self.simplified)
    def __repr__(self): return str(self)

class Distance(Unit):
    def __init__(self, value):
        super().__init__(value)
        
class m(Distance):
    label = 'm'
    example = lambda x: m(x)
    def __init__(self, value):
        super().__init__(value)
        self.conversions = {
            m: conversion(self, 1),
            km: conversion(self, 1/1000)
        }

class km(Distance):
    label = 'km'
    example = lambda x: km(x)
    def __init__(self, value):
        super().__init__(value)
        self.conversions = {
            m: conversion(self, 1000),
            km: conversion(self, 1)
        }