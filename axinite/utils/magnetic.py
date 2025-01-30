import numpy as np
import axinite as ax

def magnetic_force_modifier(charges, magnetic_field):
    """
    Returns a modifier function to calculate the magnetic force between bodies in a magnetic field.

    Args:
        charges (np.ndarray): An array mapping body indexes to their charges.
        magnetic_field (np.ndarray): The magnetic field vector.

    Returns:
        function: A modifier function to calculate the magnetic force.
    """
    def modifier(body, f, bodies, t, delta, limit, n):
        charge = charges[ax.locate_body(body, bodies)]

        for i, other in enumerate(bodies):
            other_charge = charges[i]
            if other_charge == 0:
                continue

            distance_vector = other["r"][n-1] - body["r"][n-1]
            distance = np.linalg.norm(distance_vector)

            force = charge * other_charge * np.cross(magnetic_field, distance_vector) / distance**2
            f += force
        
        return f
    return modifier
