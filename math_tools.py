import math


def sign(num: float | int) -> int:
    if num > 0:
        return 1
    elif num == 0:
        return 0
    else:
        return -1


class Vector:
    def __init__(self, x: float | int, y: float | int):
        self.x = x
        self.y = y
        self.length = math.hypot(self.x, self.y)
        self.angle = math.degrees(math.atan2(self.y, self.x))

    def rotate(self, angle: float | int):
        self.angle += angle
        angle_in_radians = math.radians(self.angle)
        if abs(self.angle) >= 360:
            self.angle %= 360
        self.x = self.length * math.cos(angle_in_radians)
        self.y = self.length * math.sin(angle_in_radians)

    def get_angle(self):
        return self.angle

    def get_coords(self):
        return self.x, self.y

    def __str__(self):
        return f"Vector({self.x}, {self.y})"

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __iadd__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __isub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Vector(self.x * other, self.y * other)

    def __imul__(self, other):
        return Vector(self.x * other, self.y * other)

    def __neg__(self):
        return Vector(-self.x, -self.y)
