from vector import Vector

def _split_float(value):
    intval = int(value)
    return intval, float(value - intval)

def _autorange(a, b):
    if a < b:
        return range(a, b + 1)
    elif b < a:
        return range(a, b - 1, -1)

    return [a]

def _line(x0, y0, x1, y1):
    if x0 == x1:
        return [(x0, y) for y in _autorange(y0, y1)]
    elif y0 == y1:
        return [(x, y0) for x in _autorange(x0, x1)]
    else:
        raise ValueError("Can't draw diagonal lines")

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
            return Vector(0, -1)
        elif direction == cls.DOWN:
            return Vector(0, 1)
        elif direction == cls.LEFT:
            return Vector(-1, 0)
        elif direction == cls.RIGHT:
            return Vector(1, 0)
        else:
            return Vector(0, 0)

class Snake(object):
    def __init__(self, initial_position=(15, 15), arena_size=(32, 32)):
        self._sections = [initial_position, (15, 16), (15, 17), (15, 18)]
        self._arena_size = arena_size
        self._speed = 1.0
        self._direction = Direction.UP
        self._offset = 0.0

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value):
        self._speed = float(value)

    @property
    def head(self):
        return self._sections[-1]

    @property
    def body(self):
        return self._sections[:-1]

    @property
    def positions(self):
        return self._sections

    def _advance(self, direction, num=1):
        for _ in range(num):
            v = Direction.to_vector(direction)
            new_head = (Vector(*self.head) + v) % Vector(*self._arena_size)
            self._sections.append((new_head.x, new_head.y))
            del self._sections[0]

    def tick(self, direction):
        if direction not in [Direction.NONE, Direction.opposite(self._direction)]:
            if self._direction != direction:
                self._offset = 0.0

            self._direction = direction
        
        self._offset += self._speed
        if self._offset >= 1.0:
            num, self._offset = _split_float(self._offset)
            self._advance(self._direction)
