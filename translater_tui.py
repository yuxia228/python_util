from curses import wrapper

msg = ""

def main(stdscr):
    global msg
    while True:
        # Clear screen
        stdscr.clear()

        stdscr.addstr(msg)
        stdscr.refresh()
        key = stdscr.getkey()
        if key == "KEY_BACKSPACE":
            msg = msg[:-1]
        else:
            msg += key

wrapper(main)

