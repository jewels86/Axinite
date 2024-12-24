import axinite as ax

class AxiniteArgs:
    def __init__(self):
        self.name = None
        self.delta = None
        self.limit = None
        self.action = None
        self.t = None
        self.bodies: list = []
        self.radius_multiplier = None
        self.rate = None
        self.retain = None
        self.modifier = None
        self.frontend_args = {}

    def unpack(self):
        return self.delta, self.limit, *self.bodies