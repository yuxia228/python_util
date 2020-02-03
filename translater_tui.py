#!/usr/bin/env python3
import curses
from curses import wrapper

msg = "sample"

def main(stdscr):
    global msg
    # Clear screen
    stdscr.clear()
    
    win_size_y, win_size_x = stdscr.getmaxyx()
    begin_y = 2
    height = win_size_y - begin_y
    width = win_size_x // 2
    editor = curses.newwin(height-2, width-2, begin_y+1, 1)
    editor.clear()
    editor_border = curses.newwin(height, width, begin_y, 0)
    editor_border.clear()

    preview = curses.newwin(height-2, width-2, begin_y+1, width+1)
    preview.clear()
    preview_border = curses.newwin(height, width, begin_y, width)
    preview_border.clear()

    refresh_list = [preview_border, editor_border, editor, preview]

    while True:
        for win in refresh_list:
            win.erase()
            pass

        preview_border.border(0, 0, 0, 0)
        editor_border.border(0, 0, 0, 0)

        preview.addstr(msg.upper())

        editor.addstr(msg)
            

        for win in refresh_list:
            win.refresh()
            pass

#        stdscr.refresh()
        key = stdscr.getkey()
        if key == "KEY_BACKSPACE":
            msg = msg[:-1]
        elif key == "KEY_UP":
            pass
        elif key == "KEY_DOWN":
            pass
        elif key == "KEY_LEFT":
            pass
        elif key == "KEY_RIGHT":
            pass
        else:
            msg += key
            msg = msg[0:width*height-1]

wrapper(main)

