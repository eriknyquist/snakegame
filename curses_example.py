import time
import sys
import curses
import threading

from snake import Direction, Snake
from framerunner import FrameRunner

HEIGHT = 34
WIDTH = 50

class config(object):
    paused = False
    direction = Direction.UP

def init_game():
    curses.initscr()
    curses.noecho()
    curses.curs_set(0)

    if curses.LINES < HEIGHT:
        height = curses.LINES
    else:
        height = HEIGHT

    if curses.COLS < WIDTH:
        width = curses.COLS
    else:
        width = WIDTH

    window = curses.newwin(height, width, 0, 0)
    window.keypad(1)

    snake = Snake(arena_size=(width - 2, height - 2))
    snake.speed = 0.2
    snake.snake_increment = 2

    return window, snake

def input_loop(win):
    while True:
        key = win.getch()
        if key == curses.KEY_UP:
            config.direction = Direction.UP
        elif key == curses.KEY_DOWN:
            config.direction = Direction.DOWN
        elif key == curses.KEY_LEFT:
            config.direction = Direction.LEFT
        elif key == curses.KEY_RIGHT:
            config.direction = Direction.RIGHT

def draw_snake(win, snake):
    for x, y in snake.positions:
        try:
            win.addstr(int(y + 1), int(x + 1), '#')
        except curses.error as e:
            pass

def draw_screen(win, snake):
    win.clear()
    win.border(0)

    draw_snake(win, snake)

    if snake.bonus_visible:
        bx, by = snake.bonus
        win.addch(int(by + 1), int(bx + 1), '*')

    ax, ay = snake.apple
    win.addch(int(ay + 1), int(ax + 1), 'A')
    win.addstr(0, 0, "Score: %d" % snake.score)
    win.refresh()

def do_screen_update(runner, win, snake):
    if not config.paused:
        if not snake.process_input(config.direction):
            runner.stop()
            time.sleep(2.0)
            curses.endwin()
            sys.exit(0)

    draw_screen(win, snake)

def main():
    window, snake = init_game()
    inputthread = threading.Thread(target=input_loop, args=(window,))
    inputthread.daemon = True
    inputthread.start()

    runner = FrameRunner(30, do_screen_update)
    runner.set_args((runner, window, snake))
    runner.run()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        curses.endwin()
