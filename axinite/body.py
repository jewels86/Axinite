from misura.quantities import quantity

class Body:
    def __init__(self, mass: quantity, volume: quantity, label: str, ):
        self.mass = mass
        self.volume = volume