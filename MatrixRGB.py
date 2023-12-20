#Author: Kaskobi (Kaskobian Softworks LLC)
#Copywrite: Florida Institute of Technology Open Source Community
#Copywrite: MIT License

import curses
from curses import wrapper
import random
import time

# Matrix characters
matrix_chars = [chr(int('0x30A0', 16) + i) for i in range(96)] + ['0', '1']

def get_rainbow_color(phase):
    """Get the RGB value for a specific phase in the rainbow."""
    if phase < 85:
        return (255 - phase * 3, phase * 3, 0)
    elif phase < 170:
        phase -= 85
        return (0, 255 - phase * 3, phase * 3)
    else:
        phase -= 170
        return (phase * 3, 0, 255 - phase * 3)

def draw_matrix(stdscr):
    curses.curs_set(0)
    curses.start_color()
    stdscr.nodelay(True)

    sh, sw = stdscr.getmaxyx()
    w = curses.newwin(sh, sw, 0, 0)
    w.timeout(0)

    drop_pos = [-1] * sw
    phase = 0

    while True:
        w.erase()
        r, g, b = get_rainbow_color(phase)
        curses.init_color(1, int(r / 255 * 1000), int(g / 255 * 1000), int(b / 255 * 1000))
        curses.init_pair(1, 1, 0)

        for i in range(sw):
            if drop_pos[i] < 0 or drop_pos[i] >= sh:
                drop_pos[i] = 0
            if drop_pos[i] > 0:
                try:
                    w.addstr(drop_pos[i] - 1, i, ' ', curses.color_pair(1))
                except curses.error:
                    pass
            char = random.choice(matrix_chars)
            try:
                w.addstr(drop_pos[i], i, char, curses.color_pair(1))
            except curses.error:
                pass
            if random.random() > 0.975:
                drop_pos[i] = 0
            else:
                drop_pos[i] += 1

        phase = (phase + 1) % 255
        w.refresh()
        curses.napms(1)

wrapper(draw_matrix)
