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
window.keypad(1)

class config(object):
    paused = False
    direction = Direction.UP

def input_loop():
    while True:
        key = window.getch()
        if key == curses.KEY_UP:
            config.direction = Direction.UP
        elif key == curses.KEY_DOWN:
            config.direction = Direction.DOWN
        elif key == curses.KEY_LEFT:
            config.direction = Direction.LEFT
        elif key == curses.KEY_RIGHT:
            config.direction = Direction.RIGHT

def _drawsnake(win, snake):
    for x, y in snake.positions:
        try:
            win.addstr(int(y), int(x), '#')
        except curses.error as e:
            pass

def _draw_screen():
    window.clear()
    window.border(0)

    _drawsnake(window, snake)

    if snake.bonus_visible:
        bx, by = snake.bonus
        window.addch(int(by), int(bx), '*')

    ax, ay = snake.apple
    window.addch(int(ay), int(ax), 'A')
    window.addstr(0, 0, "%d" % snake.score)
    window.refresh()

def do_screen_update(runner):
    if not config.paused:
        if not snake.process_input(config.direction):
            runner.stop()
            time.sleep(2.0)
            curses.endwin()
            sys.exit(0)

    _draw_screen()

def main():
    inputthread = threading.Thread(target=input_loop)
    inputthread.daemon = True
    inputthread.start()

    runner = FrameRunner(30, do_screen_update)
    runner.set_args((runner,))
    runner.run()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        curses.endwin()
