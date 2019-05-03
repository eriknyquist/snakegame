import time
import sys
import curses
import threading

from snake import Direction, Snake
from framerunner import FrameRunner
from inputs import get_gamepad

HEIGHT = 32
WIDTH = 32

curses.initscr()
curses.noecho()
curses.curs_set(0)
snake = Snake(arena_size=(WIDTH,HEIGHT))
snake.speed = 0.2
snake.snake_increment = 2

window = curses.newwin(HEIGHT, WIDTH, 0, 0)
window.nodelay(1)

class config(object):
    paused = False
    direction = Direction.UP

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

            if event.code == "BTN_START" and event.state == 1:
                config.paused = not config.paused

            config.direction = _input_id(event.code, event.state)

def draw_screen(runner):
    window.clear()
    window.border(0)

    if not config.paused:
        if not snake.process_input(config.direction):
            time.sleep(2.0)
            runner.stop()
            curses.endwin()
            sys.exit(0)

    try:
        for x, y in snake.positions:
            window.addstr(int(y), int(x), '#')
    except curses.error as e:
        pass

    if snake.bonus_visible:
        bx, by = snake.bonus
        window.addch(int(by), int(bx), '*')

    ax, ay = snake.apple
    window.addch(int(ay), int(ax), 'A')
    window.addstr(0, 0, "%d" % snake.score)
    window.refresh()

def main():
    inputthread = threading.Thread(target=input_loop)
    inputthread.daemon = True
    inputthread.start()

    runner = FrameRunner(30, draw_screen)
    runner.set_args((runner,))
    runner.run()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        curses.endwin()
