import numpy as np
from numpy.linalg import norm
from numpy.typing import NDArray
from math import cos, sin

MAX_MERGE_ANGLE = 9
MAX_OPENING_ANGLE = 136
MAX_PROJECTED_ANGLE = 121
MIN_PROJECTED_ANGLE = 59


class BeamNode:
    def __init__(self, g1: NDArray, g2: NDArray):
        self.g1 = g1
        self.g2 = g2


class ShellNode:
    def __init__(self, h: NDArray):
        self.h = h


def uvec(v: NDArray):
    return v / norm(v)


def calc_rotation_matrix_from_vector_angle(
    vec: NDArray,
    angle: float,
):
    """
    Find the rotation matrix from a rotation vector and angle
    :param vec: A 3d rotation vector.
    :param angle: A rotation angle around the rotation vector.
    :return mat: A transform matrix (3x3) which realizes a rotation of an entity around a rotation vector.
    """
    v = uvec(vec)
    kmat = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    rot = np.eye(3) + sin(angle) * kmat + (1 - cos(angle)) * kmat.dot(kmat)
    return rot


def calc_angle(v1: NDArray, v2: NDArray):
    a = (v1 @ v2) / (norm(v1) * norm(v2))
    return np.acos(max(-1, min(1, a)))


def calc_rotation_matrix_from_vectors(
    source_vec: NDArray,
    dest_vec: NDArray,
    tol: float = 1e-14,
    default_rotation_axis: NDArray = np.array([0, 1, 0], dtype="float"),
):
    """
    Find the rotation matrix that aligns "source_vec" to "dest_vec"
    :param source_vec: A 3d "source" vector
    :param dest_vec: A 3d "destination" vector
    :return mat: A transform matrix (3x3) which when applied to "source_vec", aligns it with "dest_vec".
    """
    a = source_vec
    b = dest_vec
    angle = calc_angle(a, b)
    v = np.cross(a, b)
    if not any(abs(v) > tol):
        v = default_rotation_axis
    return calc_rotation_matrix_from_vector_angle(v, angle)


def calc_parallel_projected_vec(base_vec: NDArray, vec: NDArray):
    """
    Calculate the projected vector parallel to the base vector "base_vec"
    :param base_vec: A 3d "base" vector that defines the projected direction
    :param vec: A 3d vector to be projected
    :return vector: The projected vector onto the direction defined by the base vector "base_vec"
    """
    norm_base = norm(base_vec)
    return base_vec * ((vec @ base_vec) / norm_base**2)


def calc_perpend_projected_vec(base_vec: NDArray, vec: NDArray):
    """
    Calculate the projected vector perpendicular to the base vector "base_vec"
    :param base_vec: A 3d "base" vector perpendicular to the plane of projection
    :param vec: A 3d vector to be projected
    :return vector: The projected vector perpendicular to the base vector "base_vec"
    """
    v = vec - base_vec
    return v - calc_parallel_projected_vec(base_vec, v)
