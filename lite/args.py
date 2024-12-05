import axinite as ax

class AxiniteArgs:
    def __init__(self):
        self.delta = None
        self.limit = None
        self.action = None
        self.t = None
        self.bodies: list = []
        self.radius_multiplier = None

    def unpack(self):
        return self.delta, self.limit, self.action, *self.bodies