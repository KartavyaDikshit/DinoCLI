"""
PINGPONG DELUXE - 8-Bit Edition
Controls: [W/S] Left Player, [UP/DOWN] Right Player, [R] Restart
"""

import curses
import time
import random

PADDLE_H = 4
BALL = "█"
FPS = 60

LOGO_MAIN = [
    r" ██████╗ ██╗███╗   ██╗ ██████╗      ██████╗  ██████╗ ███╗   ██╗ ██████╗  ██████╗██╗     ██╗",
    r" ██╔══██╗██║████╗  ██║██╔════╝      ██╔══██╗██╔═══██╗████╗  ██║██╔════╝ ██╔════╝██║     ██║",
    r" ██████╔╝██║██╔██╗ ██║██║  ███╗     ██████╔╝██║   ██║██╔██╗ ██║██║  ███╗██║     ██║     ██║",
    r" ██╔═══╝ ██║██║╚██╗██║██║   ██║     ██╔═══╝ ██║   ██║██║╚██╗██║██║   ██║██║     ██║     ██║",
    r" ██║     ██║██║ ╚████║╚██████╔╝     ██║     ╚██████╔╝██║ ╚████║╚██████╔╝╚██████╗███████╗██║",
    r" ╚═╝     ╚═╝╚═╝  ╚═══╝ ╚═════╝      ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝  ╚═════╝╚══════╝╚═╝"
]

def draw_shadow_text(stdscr, y, x, lines, color_pair, shadow_pair):
    for i, line in enumerate(lines):
        try:
            stdscr.addstr(y + i + 1, x + 1, line, curses.color_pair(shadow_pair))
            stdscr.addstr(y + i, x, line, curses.color_pair(color_pair) | curses.A_BOLD)
        except: pass

class Pong:
    def __init__(self, h, sw):
        self.h, self.sw = h, sw
        self.p1_y = h // 2 - 2
        self.p2_y = h // 2 - 2
        self.reset_ball()
        self.s1, self.s2 = 0, 0

    def reset_ball(self):
        self.bx, self.by = self.sw // 2, self.h // 2 + 3
        self.vx = 0.8 if random.random() > 0.5 else -0.8
        self.vy = 0.4 if random.random() > 0.5 else -0.4

    def update(self, key):
        if key == ord('w') and self.p1_y > 8: self.p1_y -= 1
        if key == ord('s') and self.p1_y < self.h - PADDLE_H: self.p1_y += 1
        if key == curses.KEY_UP and self.p2_y > 8: self.p2_y -= 1
        if key == curses.KEY_DOWN and self.p2_y < self.h - PADDLE_H: self.p2_y += 1

        self.bx += self.vx
        self.by += self.vy

        if self.by <= 8 or self.by >= self.h - 1: self.vy *= -1

        if int(self.bx) == 3 and self.p1_y <= self.by <= self.p1_y + PADDLE_H:
            self.vx = abs(self.vx) + 0.05
            self.vy += (random.random() - 0.5) * 0.2
        if int(self.bx) == self.sw - 4 and self.p2_y <= self.by <= self.p2_y + PADDLE_H:
            self.vx = -abs(self.vx) - 0.05
            self.vy += (random.random() - 0.5) * 0.2

        if self.bx < 0:
            self.s2 += 1
            self.reset_ball()
        elif self.bx > self.sw:
            self.s1 += 1
            self.reset_ball()
        
        return self.s1 < 10 and self.s2 < 10

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(1000 // FPS)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)

    while True:
        sh, sw = stdscr.getmaxyx()
        game = Pong(sh - 2, sw)
        state = "PLAYING"

        while state == "PLAYING":
            key = stdscr.getch()
            if key in [ord('q'), ord('Q')]: return
            if not game.update(key): state = "GAMEOVER"

            stdscr.erase()
            logo_x = (sw - len(LOGO_MAIN[0])) // 2
            draw_shadow_text(stdscr, 1, logo_x, LOGO_MAIN, 1, 3)

            for y in range(8, sh - 2, 2): stdscr.addstr(y, sw // 2, "╎")
            for i in range(PADDLE_H):
                stdscr.addstr(int(game.p1_y) + i, 2, "█")
                stdscr.addstr(int(game.p2_y) + i, sw - 3, "█")
            if 8 <= int(game.by) < sh - 2 and 0 <= int(game.bx) < sw:
                stdscr.addstr(int(game.by), int(game.bx), BALL)
            
            stdscr.addstr(sh - 2, sw // 2 - 10, f"P1: {game.s1}   P2: {game.s2}", curses.A_BOLD)
            stdscr.refresh()

        stdscr.addstr(sh // 2 + 5, sw // 2 - 5, "GAME OVER", curses.A_REVERSE)
        stdscr.addstr(sh // 2 + 6, sw // 2 - 11, "Press 'R' to Restart", curses.A_BOLD)
        stdscr.refresh()
        while True:
            key = stdscr.getch()
            if key in [ord('r'), ord('R')]: break
            if key in [ord('q'), ord('Q')]: return

if __name__ == "__main__":
    curses.wrapper(main)
