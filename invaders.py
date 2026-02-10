"""
INVADERS PRO - 8-Bit Edition
Controls: [ARROWS] Move, [SPACE] Shoot, [R] Restart
"""

import curses
import time
import random

FPS = 60
ALIEN = "▀▄█▄▀"
PLAYER = "▄███▄"

LOGO_MAIN = [
    r" ██╗███╗   ██╗██╗   ██╗ █████╗ ██████╗ ███████╗██████╗ ███████╗ ██████╗██╗     ██╗",
    r" ██║████╗  ██║██║   ██║██╔══██╗██╔══██╗██╔════╝██╔══██╗██╔════╝██╔════╝██║     ██║",
    r" ██║██╔██╗ ██║██║   ██║███████║██║  ██║█████╗  ██████╔╝███████╗██║     ██║     ██║",
    r" ██║██║╚██╗██║╚██╗ ██╔╝██╔══██║██║  ██║██╔══╝  ██╔══██╗╚════██║██║     ██║     ██║",
    r" ██║██║ ╚████║ ╚████╔╝ ██║  ██║██████╔╝███████╗██║  ██║███████║╚██████╗███████╗██║",
    r" ╚═╝╚═╝  ╚═══╝  ╚═══╝  ╚═╝  ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝╚══════╝ ╚═════╝╚══════╝╚═╝"
]

def draw_shadow_text(stdscr, y, x, lines, color_pair, shadow_pair):
    for i, line in enumerate(lines):
        try:
            stdscr.addstr(y + i + 1, x + 1, line, curses.color_pair(shadow_pair))
            stdscr.addstr(y + i, x, line, curses.color_pair(color_pair) | curses.A_BOLD)
        except: pass

class Invaders:
    def __init__(self, h, w):
        self.h, self.w = h, w
        self.px = w // 2
        self.bullets = []
        self.bombs = []
        self.aliens = []
        self.setup_aliens()
        self.dir = 1
        self.timer = 0
        self.score = 0

    def setup_aliens(self):
        for y in range(8, 14, 2):
            for x in range(5, self.w - 12, 6):
                self.aliens.append([float(x), y])

    def update(self, key):
        if key == curses.KEY_LEFT and self.px > 1: self.px -= 1
        if key == curses.KEY_RIGHT and self.px < self.w - 6: self.px += 1
        if key == ord(' ') and len(self.bullets) < 3:
            self.bullets.append([self.px + 2, self.h - 3])

        self.timer += 1
        move_freq = max(2, 30 - (self.score // 40))
        if self.timer % move_freq == 0:
            shift = False
            for a in self.aliens:
                if (self.dir == 1 and a[0] >= self.w - 7) or (self.dir == -1 and a[0] <= 1):
                    self.dir *= -1
                    shift = True
                    break
            for a in self.aliens:
                if shift: a[1] += 1
                else: a[0] += self.dir
                if a[1] >= self.h - 3: return "LOST"

        for b in self.bullets[:]:
            b[1] -= 0.6
            if b[1] < 8: self.bullets.remove(b)
            else:
                for a in self.aliens[:]:
                    if abs(b[0] - (a[0] + 2)) < 3 and int(b[1]) == a[1]:
                        self.aliens.remove(a)
                        if b in self.bullets: self.bullets.remove(b)
                        self.score += 10
                        break
        
        for b in self.bombs[:]:
            b[1] += 0.4
            if b[1] >= self.h - 1: self.bombs.remove(b)
            elif int(b[1]) == self.h - 2 and abs(b[0] - (self.px + 2)) < 3: return "LOST"

        if self.aliens and random.random() < 0.02:
            a = random.choice(self.aliens)
            self.bombs.append([a[0] + 2, a[1] + 1])
        
        return "WON" if not self.aliens else "PLAYING"

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(1000 // FPS)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLACK)

    while True:
        sh, sw = stdscr.getmaxyx()
        game = Invaders(sh - 2, sw)
        state = "PLAYING"

        while state == "PLAYING":
            key = stdscr.getch()
            if key in [ord('q'), ord('Q')]: return
            res = game.update(key)
            if res != "PLAYING": state = res

            stdscr.erase()
            logo_x = (sw - len(LOGO_MAIN[0])) // 2
            draw_shadow_text(stdscr, 1, logo_x, LOGO_MAIN, 5, 4)

            try:
                stdscr.addstr(game.h - 2, game.px, PLAYER, curses.color_pair(1))
                for a in game.aliens: stdscr.addstr(int(a[1]), int(a[0]), ALIEN, curses.color_pair(2))
                for b in game.bullets: stdscr.addstr(int(b[1]), int(b[0]), "┃", curses.color_pair(3))
                for b in game.bombs: stdscr.addstr(int(b[1]), int(b[0]), "░", curses.color_pair(2))
                stdscr.addstr(7, 2, f"SCORE: {game.score}", curses.A_BOLD)
            except: pass
            stdscr.refresh()

        msg = "YOU WIN!" if state == "WON" else "GAME OVER"
        stdscr.addstr(sh // 2 + 5, sw // 2 - 4, msg, curses.A_REVERSE)
        stdscr.addstr(sh // 2 + 6, sw // 2 - 11, "Press 'R' to Restart", curses.A_BOLD)
        stdscr.refresh()
        while True:
            key = stdscr.getch()
            if key in [ord('r'), ord('R')]: break
            if key in [ord('q'), ord('Q')]: return

if __name__ == "__main__":
    curses.wrapper(main)
