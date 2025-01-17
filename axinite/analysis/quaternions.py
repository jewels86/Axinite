import axinite as ax
import axinite.analysis as axana
import numpy as np
from numba import jit
@jit
def quaternion_multiply(q1, q2):
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2
    w = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
    x = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
    y = w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2
    z = w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2
    return np.array([w, x, y, z])

@jit
def quaternion_conjugate(q):
    return np.array([q[0], -q[1], -q[2], -q[3]])

@jit
def quaternion_between(v1, v2):
    u1 = ax.unit_vector_jit(v1)
    u2 = ax.unit_vector_jit(v2)

    if np.allclose(u1, u2):
        return np.array([1.0, 0.0, 0.0, 0.0])

    axis = np.cross(u1, u2)
    if np.linalg.norm(axis) == 0:
        axis = np.array([1.0, 0.0, 0.0])
    angle = axana.angle_between(u1, u2)

    w = np.cos(angle / 2)
    v = np.sin(angle / 2) * axis
    return np.array([w, *v])

@jit
def apply_quaternion(v, q):
    if np.allclose(q, np.array([1.0, 0.0, 0.0, 0.0], dtype='float64')):
        return v
    
    v_q = np.array([0.0, *v])
    
    q_conj = quaternion_conjugate(q)
    q_inv = q_conj / np.linalg.norm(q_conj)**2
    rotated = quaternion_multiply(quaternion_multiply(q, v_q), q_inv)
    return rotated[1:]

@jit
def clip_quaternion(q, radians):
    angle = 2 * np.arccos(q[0])
    max_angle = radians

    if angle > max_angle:
        angle = max_angle

    axis = q[1:]
    axis = axis / np.linalg.norm(axis)

    w = np.cos(angle / 2)
    v = np.sin(angle / 2) * axis

    return np.array([w, *v])

@jit
def clip_quaternion_degrees(q, degrees):
    return clip_quaternion(q, np.radians(degrees))