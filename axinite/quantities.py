from axinite.measurements import Measurement

class Vector3:
    def __init__(self, x: Measurement, y: Measurement, z: Measurement):
        self.x = x
        self.y = y
        self.z = z
