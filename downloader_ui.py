#!/usr/bin/env python3
import curses

class DownloaderUI:
    def __init__(self, stdscr):
        # Init all windows
        self.stdscr = stdscr
        self.stdscr.resize(5, 5)
        self.stdscr.box()
        self.list_root_win = curses.newwin(curses.LINES-3, 32, 0, 0) #pylint: disable=no-member
        self.list_root_win.box()
        self.mod_list_win = curses.newwin(curses.LINES-9, 30, 5, 1) #pylint: disable=no-member
        self.controls_win = curses.newwin(3, 32, curses.LINES-3, 0) #pylint: disable=no-member
        self.status_win = curses.newwin(6, curses.COLS-32, 0, 32) #pylint: disable=no-member
        self.status_win.box()
        self.command_win = curses.newwin(curses.LINES-6, curses.COLS-32, 6, 32) #pylint: disable=no-member
        self.command_win.box()
        self.cmd_output_win = curses.newwin(curses.LINES-10, curses.COLS-34, 7, 33) #pylint: disable=no-member

        # Populate list_root_win
        self.list_root_win.addstr(1, 1, 'Mod count:')
        self.list_root_win.addstr(2, 1, 'Optional:')

        # Populate mod_list_win
        self.mod_list_win.addstr(0, 0, '>Test Filename') # test
        self.mod_list_win.addstr(0, 27, '[x]')

        # Populate controls_win
        self.controls_win.addstr(0, 0, 'x or <RETURN> to check/uncheck')
        self.controls_win.addstr(1, 0, 'j/k or Up/Down to select')
        self.controls_win.addstr(2, 1, '<ESC> or q to quit')

        # Populate status_win
        self.status_win.addstr(1, 1, 'Current mod list: <filename or url>')
        self.status_win.addstr(2, 1, 'Modpack name: <name or N/A> Status: <status>')
        self.status_win.addstr(3, 1, 'Game dir: <path>')
        self.status_win.addstr(4, 1, 'Current file: <filename>')

        # Populate command_win
        self.command_win.addstr(self.command_win.getmaxyx()[0]-2, 1, '> ')

        self.refresh_all()

        # Wait
        stdscr.getch()

    def set_mod_count(self, mod_count: int):
        self.list_root_win.move(1, 12)
        self.list_root_win.clrtoeol()
        self.list_root_win.box()
        self.list_root_win.addstr(1, 12, str(mod_count))

    def set_optional_count(self, enabled_cnt: int, all_cnt: int):
        self.list_root_win.addstr(2, 11, '         ')
        self.list_root_win.addstr(2, 11, '{}/{}'.format(enabled_cnt, all_cnt))

    def refresh_all(self):
        self.stdscr.refresh()
        self.list_root_win.refresh()
        self.mod_list_win.refresh()
        self.controls_win.refresh()
        self.status_win.refresh()
        self.command_win.refresh()
        self.cmd_output_win.refresh()

    def start(self):
        pass

def main(stdscr):
    dui = DownloaderUI(stdscr)
    dui.set_mod_count(15)
    dui.refresh_all()
    dui.stdscr.getch()
    dui.start()

curses.wrapper(main)
