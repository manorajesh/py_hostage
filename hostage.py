import curses
from random import randint, choice
import re
from threading import Thread
from time import sleep

class Hostage():
    def __init__(self):
        self.stdscr = curses.initscr()
        self.stdscr.keypad(True)
        curses.curs_set(0)
        curses.noecho()

        self.display = []

        self.init_display()
        self.get_input()
        self.exit()

    def init_display(self):
        self.lines, self.columns = self.stdscr.getmaxyx()
        self.lines -= 1
        self.columns //= 3
        self.charset = "ABCDEFGIJKLMNOPQRSTUVWXYZ"

        randnum = randint(0, self.columns-1)
        for i in range(self.lines):
            self.display.append("K" * self.columns)
            self.display[i] = self.display[i][:randnum] + "H" + self.display[i][randnum+1:]
            randnum = randint(0, self.lines-1)

        for i, val in enumerate(self.display):
            self.stdscr.addstr(i, self.columns, val, curses.A_DIM)
        self.stdscr.addstr(self.lines, self.columns, "R")

    def get_input(self):
        self.player_x = self.columns
        self.player_y = self.lines

        try:
            while ((ch := self.stdscr.getch()) != ord("q")):
                if ch == curses.KEY_LEFT:
                    self.player_x = self.player_x - 1 if self.columns < self.player_x else self.columns*2-1
                elif ch == curses.KEY_RIGHT:
                    self.player_x = self.player_x + 1 if self.player_x < self.columns*2-1 else self.columns
                elif ch == curses.KEY_UP:
                    if list(self.display[self.player_y-1])[self.player_x-self.columns] == "H":
                        self.player_y -= 1 
                        del self.display[self.player_y]
                
                self.update_display()
        except IndexError:
            self.exit()
                
    def update_display(self):
        self.stdscr.clear()
        for i, val in enumerate(self.display):
            self.stdscr.addstr(i, self.columns, re.sub(rf"[{self.charset}]", choice(self.charset), val))
        self.stdscr.addstr(self.player_y, self.player_x, "R")
        self.stdscr.refresh()

    def exit(self):
        curses.curs_set(1)
        curses.echo()
        curses.endwin()

if __name__ == "__main__":
    test = Hostage()