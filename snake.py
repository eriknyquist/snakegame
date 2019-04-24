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

class Direction(object):
    NONE = -1
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

    @classmethod
    def opposite(cls, direction):
        if direction == cls.UP:
            return cls.DOWN
        elif direction == cls.DOWN:
            return cls.UP
        elif direction == cls.LEFT:
            return cls.RIGHT
        elif direction == cls.RIGHT:
            return cls.LEFT
        else:
            return None

    @classmethod
    def to_vector(cls, direction):
        if direction == cls.UP:
            return Vector(0, 1)
        elif direction == cls.DOWN:
            return Vector(0, -1)
        elif direction == cls.LEFT:
            return Vector(-1, 0)
        elif direction == cls.RIGHT:
            return Vector(1, 0)
        else:
            return Vector(0, 0)

class Snake(object):
    def __init__(self, initial_position=Vector(15, 15), arena_size=(32, 32)):
        self._sections = [initial_position]
        self._arena_size = arena_size
        self._speed = 1.0
        self._direction = Direction.UP
        self._vector = None
        self._calculate_vector()

    def _calculate_vector(self):
        self._vector = Direction.to_vector(self._direction) * self._speed

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value):
        self._speed = float(value)
        self._calculate_vector()

    @property
    def head(self):
        return self._sections[0]

    @property
    def body(self):
        return self._sections[1:]

    def tick(self, speed, direction):
        if direction not in [Direction.NONE, Direction.opposite(self._direction)]:
            self._direction = direction
            self._calculate_vector()

        new_head = Vector(*self.head) + self._vector
