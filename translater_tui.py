#!/usr/bin/env python3
import curses
from curses import wrapper
import threading
import libtrans
trans = libtrans.Translate()

msg = "sample"
trans_msg = ""

ThreadEnd = False
def thread_translate():
    global trans_msg
    while ThreadEnd is not True:
        trans_msg = trans.google_translate(msg)

def main(stdscr):
    global msg
    global ThreadEnd

    TIME_OUT=100 # getkeyのtimeout時間(refreshレート)

    # Clear screen
    stdscr.clear()
    stdscr.timeout(TIME_OUT)

    win_size_y, win_size_x = stdscr.getmaxyx()
    begin_y = 2
    height = win_size_y - begin_y
    width = win_size_x // 2
    editor = curses.newwin(height-2, width-2, begin_y+1, 1)
    editor.clear()
    editor_border = curses.newwin(height, width, begin_y, 0)
    editor_border.clear()
    editor.timeout(TIME_OUT)

    preview = curses.newwin(height-2, width-2, begin_y+1, width+1)
    preview.clear()
    preview_border = curses.newwin(height, width, begin_y, width)
    preview_border.clear()
    preview.timeout(TIME_OUT)

    refresh_list = [preview_border, editor_border, editor, preview]

    # start  translate thread
    thread = threading.Thread(target=thread_translate)
    thread.start()

    try:
        while True:
            for win in refresh_list:
                win.erase()
                pass

            preview_border.border(0, 0, 0, 0)
            editor_border.border(0, 0, 0, 0)

            preview.addstr(trans_msg)

            editor.addstr(msg) 

            for win in refresh_list:
                win.refresh()
                pass

            try:
                key = stdscr.getkey()
            except curses.error:
                continue

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
    except KeyboardInterrupt:
        ThreadEnd = True
        thread.join()

wrapper(main)

