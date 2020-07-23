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
        self.list_info_win = curses.newwin(3, 30, 1, 1)
        self.mod_list_win = curses.newwin(curses.LINES-9, 30, 5, 1) #pylint: disable=no-member
        self.controls_win = curses.newwin(3, 32, curses.LINES-3, 0) #pylint: disable=no-member
        self.status_win = curses.newwin(6, curses.COLS-32, 0, 32) #pylint: disable=no-member
        self.status_win.box()
        self.status_container_win = curses.newwin(4, curses.COLS-34, 1, 33) #pylint: disable=no-member
        self.command_win = curses.newwin(curses.LINES-6, curses.COLS-32, 6, 32) #pylint: disable=no-member
        self.command_win.box()
        self.cmd_prompt_win = curses.newwin(2, curses.COLS-34, curses.LINES-3, 33) #pylint: disable=no-member
        self.cmd_output_win = curses.newwin(curses.LINES-10, curses.COLS-34, 7, 33) #pylint: disable=no-member

        # Populate list_root_win
        self.list_info_win.addstr(0, 0, 'Mod count:')
        self.list_info_win.addstr(1, 0, 'Optional:')

        # Populate mod_list_win
        self.mod_list_win.addstr(0, 0, '>Test Filename') # test
        self.mod_list_win.addstr(0, 27, '[x]')

        # Populate controls_win
        self.controls_win.addstr(0, 0, 'x or <RETURN> to check/uncheck')
        self.controls_win.addstr(1, 0, 'j/k or Up/Down to select')
        self.controls_win.addstr(2, 1, '<ESC> or q to quit')

        # Populate status_container_win
        self.status_container_win.addstr(0, 0, 'Current mod list: <filename or url>')
        self.status_container_win.addstr(1, 0, 'Modpack name: <name or N/A>          Status: <status>')
        self.status_container_win.addstr(2, 0, 'Game dir: <path>')
        self.status_container_win.addstr(3, 0, 'Current file: <filename>')

        # Populate cmd_prompt_win
        self.cmd_prompt_win.addstr(1, 0, '> ')

        self.refresh_all()

        # Wait
        stdscr.getch()

    def set_mod_count(self, mod_count: int):
        self.list_info_win.move(0, 11)
        self.list_info_win.clrtoeol()
        self.list_info_win.addstr(0, 11, str(mod_count))

    def set_optional_count(self, enabled_cnt: int, all_cnt: int):
        self.list_info_win.move(1, 10)
        self.list_info_win.clrtoeol()
        self.list_info_win.addstr(1, 10, '{}/{}'.format(enabled_cnt, all_cnt))

    def set_modlist_name(self, modlist_name: str):
        self.status_container_win.move(0, 18)
        self.status_container_win.clrtoeol()
        self.status_container_win.addstr(0, 18, modlist_name)

    def set_modpack_name(self, modpack_name: str):
        self.status_container_win.addstr(1, 14, '                      ') # Clear previous contents
        self.status_container_win.addstr(1, 14, modpack_name) # TODO: Add check for name lengh. Must be 22 or less. And also change the max size maybe

    def set_status(self, status: str):
        self.status_container_win.addstr(1, 45, '           ')
        self.status_container_win.addstr(1, 45, status)

    def set_game_dir(self, game_dir: str):
        self.status_container_win.move(2, 10)
        self.status_container_win.clrtoeol()
        self.status_container_win.addstr(2, 10, game_dir)

    def set_current_file(self, filename: str):
        self.status_container_win.move(3, 14)
        self.status_container_win.clrtoeol()
        self.status_container_win.addstr(3, 14, filename)

    def refresh_all(self):
        self.stdscr.refresh()
        self.list_root_win.refresh()
        self.list_info_win.refresh()
        self.mod_list_win.refresh()
        self.controls_win.refresh()
        self.status_win.refresh()
        self.status_container_win.refresh()
        self.command_win.refresh()
        self.cmd_prompt_win.refresh()
        self.cmd_output_win.refresh()

if __name__ == '__main__':
    def main(stdscr):
        dui = DownloaderUI(stdscr)
        dui.set_mod_count(15)
        dui.set_optional_count(5, 10)
        dui.set_modlist_name('Test Filename')
        dui.set_modpack_name('TBN3')
        dui.set_status('downloading')
        dui.set_game_dir('/home/jtcf/.minecraft/home/tbn3/')
        dui.set_current_file('Test Filename.jar')
        dui.refresh_all()
        dui.stdscr.getch()

    curses.wrapper(main)
