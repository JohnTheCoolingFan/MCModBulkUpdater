#!/usr/bin/env python3
import curses

def main(stdscr):
    stdscr.clear()
    stdscr.box()
    stdscr.getch()

curses.wrapper(main)
