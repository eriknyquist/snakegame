import sys
import curses
import threading

from snake import Direction, Snake
from framerunner import FrameRunner
from inputs import get_gamepad

HEIGHT = 32
WIDTH = 48

curses.initscr()
curses.noecho()
curses.curs_set(0)
snake = Snake(arena_size=(WIDTH,HEIGHT))
snake.speed = 0.2

window = curses.newwin(HEIGHT, WIDTH, 0, 0)
window.nodelay(1)

class config(object):
    direction = Direction.UP

def quit():
    curses.endwin()
    sys.exit(0)

def _input_id(code, state):
    if state == 0:
        return Direction.NONE

    if code == "ABS_HAT0X":
        return Direction.LEFT if state < 0 else Direction.RIGHT

    if code == "ABS_HAT0Y":
        return Direction.UP if state < 0 else Direction.DOWN

    return Direction.NONE

def input_loop():
    while True:
        events = get_gamepad()
        for event in events:
            if event.ev_type not in ["Absolute", "Key"]:
                continue

            config.direction = _input_id(event.code, event.state)

def draw_screen():
    window.clear()
    window.border(0)
    if not snake.tick(config.direction):
        quit() #dead

    for x, y in snake.positions:
        window.addch(int(y), int(x), '#')

    x, y = snake.apple
    window.addch(y, x, 'A')
    window.addstr(0, 0, "%d" % snake.score)
    window.refresh()

def main():
    inputthread = threading.Thread(target=input_loop)
    inputthread.daemon = True
    inputthread.start()

    runner = FrameRunner(30, draw_screen)
    runner.run()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        quit()
