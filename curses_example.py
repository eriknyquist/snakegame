import time
import sys
import curses
import threading

from snake import Direction, Snake
from framerunner import FrameRunner

HEIGHT = 32
WIDTH = 48

curses.initscr()
curses.noecho()
curses.curs_set(0)

snake = Snake(arena_size=(WIDTH,HEIGHT))
snake.speed = 0.2
snake.snake_increment = 2

window = curses.newwin(HEIGHT + 2, WIDTH + 2, 0, 0)
window.keypad(1)

class config(object):
    paused = False
    direction = Direction.UP

def input_loop(runner):
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
            win.addstr(int(y + 1), int(x + 1), '#')
        except curses.error as e:
            pass

def _draw_screen():
    window.clear()
    window.border(0)

    _drawsnake(window, snake)

    if snake.bonus_visible:
        bx, by = snake.bonus
        window.addch(int(by + 1), int(bx + 1), '*')

    ax, ay = snake.apple
    window.addch(int(ay + 1), int(ax + 1), 'A')
    window.addstr(0, 0, "Score: %d" % snake.score)
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
    inputthread = threading.Thread(target=input_loop, args=(runner,))
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
