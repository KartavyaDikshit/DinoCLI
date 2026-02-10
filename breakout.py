"""
BREAKOUTCLI - 8-Bit Edition
Controls: [ARROWS] Move, [R] Restart, [Q] Quit
"""

import curses
import time
import random

FPS = 60
BALL = "█"
PADDLE = "██████"
BRICK = "██"

LOGO_MAIN = [
    r" ██████╗ ██████╗ ███████╗ █████╗ ██╗  ██╗ ██████╗ ██╗   ██╗████████╗ ██████╗██╗     ██╗",
    r" ██╔══██╗██╔══██╗██╔════╝██╔══██╗██║ ██╔╝██╔═══██╗██║   ██║╚══██╔══╝██╔════╝██║     ██║",
    r" ██████╔╝██████╔╝█████╗  ███████║█████╔╝ ██║   ██║██║   ██║   ██║   ██║     ██║     ██║",
    r" ██╔══██╗██╔══██╗██╔══╝  ██╔══██║██╔═██╗ ██║   ██║██║   ██║   ██║   ██║     ██║     ██║",
    r" ██████╔╝██║  ██║███████╗██║  ██║██║  ██╗╚██████╔╝╚██████╔╝   ██║   ╚██████╗███████╗██║",
    r" ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝  ╚═════╝    ╚═╝    ╚═════╝╚══════╝╚═╝"
]

def draw_shadow_text(stdscr, y, x, lines, color_pair, shadow_pair):
    for i, line in enumerate(lines):
        try:
            stdscr.addstr(y + i + 1, x + 1, line, curses.color_pair(shadow_pair))
            stdscr.addstr(y + i, x, line, curses.color_pair(color_pair) | curses.A_BOLD)
        except: pass

class Breakout:
    def __init__(self, h, w):
        self.h, self.w = h, w
        self.px = w // 2 - 3
        self.bx, self.by = float(w // 2), float(h - 5)
        self.vx, self.vy = 0.6, -0.4
        self.bricks = []
        for y in range(8, 13):
            for x in range(2, w - 4, 3):
                self.bricks.append([x, y, random.randint(3, 5)])
        self.score = 0
        self.lives = 3

    def update(self, key):
        if key == curses.KEY_LEFT and self.px > 1: self.px -= 2
        if key == curses.KEY_RIGHT and self.px < self.w - 7: self.px += 2

        self.bx += self.vx
        self.by += self.vy

        # Walls
        if self.bx <= 1 or self.bx >= self.w - 2: self.vx *= -1
        if self.by <= 8: self.vy *= -1

        # Paddle
        if int(self.by) == self.h - 3 and self.px <= self.bx <= self.px + 6:
            self.vy = -abs(self.vy)
            self.vx += (self.bx - (self.px + 3)) * 0.1

        # Bricks
        for b in self.bricks[:]:
            if int(self.by) == b[1] and b[0] <= self.bx <= b[0] + 2:
                self.bricks.remove(b)
                self.vy *= -1
                self.score += 50
                break

        if self.by >= self.h:
            self.lives -= 1
            self.bx, self.by = float(self.px + 3), float(self.h - 5)
            self.vy = -0.4
            if self.lives <= 0: return False
        return True

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(1000 // FPS)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_RED, curses.COLOR_BLACK)

    while True:
        sh, sw = stdscr.getmaxyx()
        game = Breakout(sh, sw)
        
        while True:
            key = stdscr.getch()
            if key in [ord('q'), ord('Q')]: return
            if not game.update(key): break
            if not game.bricks: break

            stdscr.erase()
            logo_x = (sw - len(LOGO_MAIN[0])) // 2
            draw_shadow_text(stdscr, 1, logo_x, LOGO_MAIN, 1, 2)

            # Draw Bricks
            for b in game.bricks:
                stdscr.addstr(b[1], b[0], BRICK, curses.color_pair(b[2]))
            
            # Draw Paddle
            stdscr.addstr(sh - 3, game.px, PADDLE, curses.color_pair(4))
            # Draw Ball
            if 0 <= int(game.by) < sh and 0 <= int(game.bx) < sw:
                stdscr.addstr(int(game.by), int(game.bx), BALL, curses.color_pair(1))

            stdscr.addstr(7, 2, f"SCORE: {game.score}   LIVES: {game.lives}", curses.A_BOLD)
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
