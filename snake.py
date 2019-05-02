import random
from vector import Vector

speed_increments = [2, 5, 10, 15, 20, 25, 30, 50]

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
        self._sections = [
            (initial_position[0], initial_position[1] - 1),
            initial_position
        ]

        self._arena_size = arena_size
        self._speed = 0.2
        self._direction = Direction.UP
        self._offset = 0.0
        self._snake_inc = 2
        self._grow = 0
        self._apples = 0
        self._score = 0
        self._apple_points = 100
        self._max_speed = 1.0
        self._speed_inc = 0.05
        self._max_apples_inc = 20
        self._distance_since_last_move = 0.0
        self._apple = (0, 0)
        self._new_apple()

    @property
    def max_speed(self):
        return self._max_speed

    @max_speed.setter
    def max_speed(self, value):
        self._max_speed = float(value)

    @property
    def speed_increment(self):
        return self._speed_inc

    @speed_increment.setter
    def speed_increment(self, value):
        self._speed_inc = float(value)

    @property
    def snake_increment(self):
        return self._snake_inc

    @snake_increment.setter
    def snake_increment(self, value):
        self._snake_inc = float(value)

    @property
    def apple(self):
        return self._apple

    @property
    def score(self):
        return self._score

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

    def _set_speed(self):
        if self._apples > speed_increments[-1]:
            if self._apples % self._max_apples_inc:
                self._speed = min(self._speed + self._speed_inc,
                        self._max_speed)

        if self._apples in speed_increments:
            self._speed = min(self._speed + self._speed_inc, self._max_speed)

    def _inc_score(self):
        self._apples += 1
        self._set_speed()
        self._score += self._apple_points * self._speed

    def _new_apple(self):
        old = self._apple
        while (self._apple == old) or (self._apple in self.positions):
            self._apple = (
                random.randrange(1, self._arena_size[0] - 1),
                random.randrange(1, self._arena_size[1] - 1)
            )

    def _advance(self, direction, num=1):
        for _ in range(num):
            v = Direction.to_vector(direction)
            new_head = (Vector(*self.head) + v) % Vector(*self._arena_size)
            self._sections.append((new_head.x, new_head.y))

            if (new_head == Vector(*self._apple)):
                self._new_apple()
                self._inc_score()
                self._grow += self._snake_inc

            if self._grow > 0:
                self._grow -= 1
            else:
                del self._sections[0]

            if new_head in self.body:
                return False

        self._distance_since_last_move += num
        return True

    def _is_new_direction(self, direction):
        if (direction in [Direction.NONE, Direction.opposite(self._direction)]):
            return False

        return direction != self._direction

    def _distance_moved(self):
        return self._distance_since_last_move + self._offset

    def process_input(self, direction):
        if self._is_new_direction(direction) and (self._distance_moved() > 1.0):
            self._offset = 0.0
            self._distance_since_last_move = 0.0
            self._direction = direction

        self._offset += self._speed
        if self._offset >= 1.0:
            num, self._offset = _split_float(self._offset)
            if not self._advance(self._direction, num):
                return False

        return True
