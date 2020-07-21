#!/usr/bin/env python3
import curses

class DownloaderUI:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.stdscr.resize(5, 5)
        self.stdscr.box()
        self.stdscr.refresh()
        self.list_root_win = curses.newwin(curses.LINES-3, 32, 0, 0)
        self.list_root_win.box()
        self.list_root_win.refresh()
        self.mod_list_win = curses.newwin(curses.LINES-9, 30, 5, 1)
        self.mod_list_win.box()
        self.mod_list_win.refresh()
        self.controls_win = curses.newwin(3, 32, curses.LINES-3, 0)
        self.controls_win.box()
        self.controls_win.refresh()
        self.status_win = curses.newwin(6, curses.COLS-32, 0, 32)
        self.status_win.box()
        self.status_win.refresh()
        self.command_win = curses.newwin(curses.LINES-6, curses.COLS-32, 6, 32)
        self.command_win.box()
        self.command_win.refresh()
        self.cmd_output_win = curses.newwin(curses.LINES-10, curses.COLS-34, 7, 33)
        self.cmd_output_win.box()
        self.cmd_output_win.refresh()
        stdscr.getch()

def main(stdscr):
    dui = DownloaderUI(stdscr)

curses.wrapper(main)
