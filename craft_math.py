"""
Math utilities for 3D graphics
Converted from matrix.c
"""

import math
import numpy as np
from typing import Tuple, List

class Vector3:
    """3D Vector class"""
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
    
    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, scalar):
        return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)
    
    def __rmul__(self, scalar):
        return self.__mul__(scalar)
    
    def __truediv__(self, scalar):
        return Vector3(self.x / scalar, self.y / scalar, self.z / scalar)
    
    def length(self):
        return math.sqrt(self.x*self.x + self.y*self.y + self.z*self.z)
    
    def normalize(self):
        length = self.length()
        if length > 0:
            return Vector3(self.x/length, self.y/length, self.z/length)
        return Vector3(0, 0, 0)
    
    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z
    
    def cross(self, other):
        return Vector3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )
    
    def to_list(self):
        return [self.x, self.y, self.z]
    
    def __repr__(self):
        return f"Vector3({self.x}, {self.y}, {self.z})"

class Matrix4:
    """4x4 Matrix class for 3D transformations"""
    
    def __init__(self, data=None):
        if data is None:
            self.data = np.identity(4, dtype=np.float32)
        else:
            self.data = np.array(data, dtype=np.float32).reshape(4, 4)
    
    @classmethod
    def identity(cls):
        """Create identity matrix"""
        return cls()
    
    @classmethod
    def translation(cls, x, y, z):
        """Create translation matrix"""
        matrix = cls.identity()
        matrix.data[0, 3] = x
        matrix.data[1, 3] = y
        matrix.data[2, 3] = z
        return matrix
    
    @classmethod
    def rotation_x(cls, angle):
        """Create rotation matrix around X axis"""
        matrix = cls.identity()
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        matrix.data[1, 1] = cos_a
        matrix.data[1, 2] = -sin_a
        matrix.data[2, 1] = sin_a
        matrix.data[2, 2] = cos_a
        return matrix
    
    @classmethod
    def rotation_y(cls, angle):
        """Create rotation matrix around Y axis"""
        matrix = cls.identity()
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        matrix.data[0, 0] = cos_a
        matrix.data[0, 2] = sin_a
        matrix.data[2, 0] = -sin_a
        matrix.data[2, 2] = cos_a
        return matrix
    
    @classmethod
    def rotation_z(cls, angle):
        """Create rotation matrix around Z axis"""
        matrix = cls.identity()
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        matrix.data[0, 0] = cos_a
        matrix.data[0, 1] = -sin_a
        matrix.data[1, 0] = sin_a
        matrix.data[1, 1] = cos_a
        return matrix
    
    @classmethod
    def perspective(cls, fov, aspect, near, far):
        """Create perspective projection matrix"""
        matrix = cls()
        f = 1.0 / math.tan(math.radians(fov) / 2.0)
        matrix.data[0, 0] = f / aspect
        matrix.data[1, 1] = f
        matrix.data[2, 2] = (far + near) / (near - far)
        matrix.data[2, 3] = (2 * far * near) / (near - far)
        matrix.data[3, 2] = -1.0
        matrix.data[3, 3] = 0.0
        return matrix
    
    @classmethod
    def ortho(cls, left, right, bottom, top, near, far):
        """Create orthographic projection matrix"""
        matrix = cls()
        matrix.data[0, 0] = 2.0 / (right - left)
        matrix.data[1, 1] = 2.0 / (top - bottom)
        matrix.data[2, 2] = -2.0 / (far - near)
        matrix.data[0, 3] = -(right + left) / (right - left)
        matrix.data[1, 3] = -(top + bottom) / (top - bottom)
        matrix.data[2, 3] = -(far + near) / (far - near)
        return matrix
    
    def __mul__(self, other):
        """Matrix multiplication"""
        if isinstance(other, Matrix4):
            result = Matrix4()
            result.data = np.dot(self.data, other.data)
            return result
        elif isinstance(other, Vector3):
            # Transform vector
            vec4 = np.array([other.x, other.y, other.z, 1.0])
            result = np.dot(self.data, vec4)
            return Vector3(result[0], result[1], result[2])
        else:
            raise TypeError("Can only multiply with Matrix4 or Vector3")
    
    def translate(self, x, y, z):
        """Apply translation"""
        translation = Matrix4.translation(x, y, z)
        self.data = np.dot(self.data, translation.data)
    
    def rotate_x(self, angle):
        """Apply rotation around X axis"""
        rotation = Matrix4.rotation_x(angle)
        self.data = np.dot(self.data, rotation.data)
    
    def rotate_y(self, angle):
        """Apply rotation around Y axis"""
        rotation = Matrix4.rotation_y(angle)
        self.data = np.dot(self.data, rotation.data)
    
    def rotate_z(self, angle):
        """Apply rotation around Z axis"""
        rotation = Matrix4.rotation_z(angle)
        self.data = np.dot(self.data, rotation.data)
    
    def inverse(self):
        """Get inverse matrix"""
        result = Matrix4()
        result.data = np.linalg.inv(self.data)
        return result
    
    def to_opengl(self):
        """Convert to OpenGL format (column-major)"""
        return self.data.T.flatten()

def normalize(x, y, z):
    """Normalize a 3D vector"""
    length = math.sqrt(x*x + y*y + z*z)
    if length > 0:
        return x/length, y/length, z/length
    return 0, 0, 0

def radians(degrees):
    """Convert degrees to radians"""
    return degrees * math.pi / 180.0

def degrees(radians):
    """Convert radians to degrees"""
    return radians * 180.0 / math.pi

def lerp(a, b, t):
    """Linear interpolation"""
    return a + t * (b - a)

def clamp(value, min_val, max_val):
    """Clamp value between min and max"""
    return max(min_val, min(max_val, value))

def chunked(x):
    """Convert world coordinate to chunk coordinate"""
    return int(math.floor(x / 32))  # CHUNK_SIZE = 32