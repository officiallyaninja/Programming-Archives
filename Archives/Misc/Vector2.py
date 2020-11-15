import numbers


class Vector2:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.components = (x, y)

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, scalar):
        if isinstance(scalar, numbers.Number):
            return Vector2(scalar * self.x, scalar * self.y)
        else:
            raise TypeError

    def __rmul__(self, scalar):
        if isinstance(scalar, numbers.Number):
            return Vector2(scalar * self.x, scalar * self.y)
        else:
            raise ValueError

    def __neg__(self):
        return Vector2(-self.x, -self.y)

    def __pos__(self):
        return Vector2(self.x, self.y)

    def __abs__(self):
        return self.magnitude()

    def __eq__(self, other):
        return self.x == other.x and self.y == self.y

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        return str(self.components)

    def __iter__(self):
        return iter(self.components)

    def magnitude(self):
        x = self.x
        y = self.y
        return((x**2 + y**2) ** (0.5))

    def dot(self, other):
        return (self.x * other.x + self.y + other.y)


velocity = Vector2(1, 2)
print(2*velocity*2)
