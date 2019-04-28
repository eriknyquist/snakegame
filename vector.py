class Vector(object):
    @classmethod
    def from_direction(cls, direction):
        return Direction.to_vector(direction)

    def __init__(self, x, y):
        self._x = float(x)
        self._y = float(y)

    def _check_type(self, operation, other):
        if not isinstance(other, Vector):
            raise ValueError("Can't %s %s and %s types"
                % (operation, type(self), type(other)))

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = float(value)

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = float(value)

    def __add__(self, other):
        self._check_type("add", other)
        return Vector(self._x + other._x, self._y + other._y)

    def __sub__(self, other):
        self._check_type("subtract", other)
        return Vector(self._x - other._x, self._y - other._y)

    def __abs__(self):
        return abs(self._x) + abs(self._y)

    def __mul__(self, other):
        if type(other) in [int, float]:
            return Vector(self._x * float(other), self._y * float(other))

        self._check_type("multiply", other)
        return Vector(self._x * other._x, self._y * other._y)

    def __mod__(self, other):
        if type(other) in [int, float]:
            return Vector(self._x % float(other), self._y % float(other))

        self._check_type("modulo", other)
        return Vector(self._x % other._x, self._y % other._y)

    def __float__(self):
        return float(self._x + self._y)

    def __int__(self):
        return int(self.__float__())

    def __str__(self):
        return "%s(x=%.2f, y=%.2f)" % (Vector.__name__, self._x, self._y)

    def __repr__(self):
        return self.__str__()

