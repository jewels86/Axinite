import numpy as np
import axinite as ax

def normal_force_modifier():
    """
    Returns a modifier function to calculate the normal force between bodies.

    Returns:
        function: A modifier function to calculate the normal force.
    """
    def modifier(body, f, bodies, t, delta, limit, n):
        for other in bodies:
            if np.array_equal(body["r"][n-1], other["r"][n-1]):
                continue

            distance_vector = other["r"][n-1] - body["r"][n-1]
            distance = np.linalg.norm(distance_vector)
            normal_vector = distance_vector / distance
            force_magnitude = body["m"] * other["m"] * ax.G / distance**2
            f += force_magnitude * normal_vector
        
        return f
    return modifier
