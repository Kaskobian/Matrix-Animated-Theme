#Author: Kaskobi (Kaskobian Softworks LLC)
#Copywrite: Florida Institute of Technology Open Source Community
#Copywrite: MIT License

import curses
from curses import wrapper
import random
import time

matrix_chars = [chr(int('0x30A0', 16) + i) for i in range(96)] + ['0', '1']

def lerp_color(start_color, end_color, transition_progress):
    """Interpolate between two colors."""
    return tuple(int(start_color[j] + (end_color[j] - start_color[j]) * transition_progress) for j in range(3))

def draw_matrix(stdscr):
    curses.curs_set(0)
    curses.start_color()
    stdscr.nodelay(True)

    sh, sw = stdscr.getmaxyx()
    w = curses.newwin(sh, sw, 0, 0)
    w.timeout(0)

    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)

    drop_pos = [-1] * sw
    start_time = time.time()
    color_transition_duration = 30
    color_number = 1

    while True:
        w.erase()
        for i in range(sw):
            if drop_pos[i] < 0 or drop_pos[i] >= sh:
                drop_pos[i] = 0
            if drop_pos[i] > 0:
                try:
                    w.addstr(drop_pos[i] - 1, i, ' ', curses.color_pair(color_number))
                except curses.error:
                    pass
            char = random.choice(matrix_chars)
            try:
                w.addstr(drop_pos[i], i, char, curses.color_pair(color_number))
            except curses.error:
                pass
            if random.random() > 0.975:
                drop_pos[i] = 0
            else:
                drop_pos[i] += 1

        current_time = time.time()
        if int(current_time) % color_transition_duration == 0:
            color_number = 2 if color_number == 1 else 1

        w.refresh()
        curses.napms(1)

wrapper(draw_matrix)