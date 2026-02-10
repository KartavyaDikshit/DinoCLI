"""
TETRIS PRO - 8-Bit Edition
Controls: [ARROWS] Move/Rotate, [SPACE] Drop, [R] Restart
"""

import curses
import time
import random

FPS = 60
BLOCK = "██"

LOGO_MAIN = [
    r" ████████╗███████╗████████╗██████╗ ██╗███████╗ ██████╗██╗     ██╗",
    r" ╚══██╔══╝██╔════╝╚══██╔══╝██╔══██╗██║██╔════╝██╔════╝██║     ██║",
    r"    ██║   █████╗     ██║   ██████╔╝██║███████╗██║     ██║     ██║",
    r"    ██║   ██╔══╝     ██║   ██╔══██╗██║╚════██║██║     ██║     ██║",
    r"    ██║   ███████╗   ██║   ██║  ██║██║███████║╚██████╗███████╗██║",
    r"    ╚═╝   ╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝╚══════╝ ╚═════╝╚══════╝╚═╝"
]

SHAPES = {
    'I': [[1, 1, 1, 1]],
    'J': [[1, 0, 0], [1, 1, 1]],
    'L': [[0, 0, 1], [1, 1, 1]],
    'O': [[1, 1], [1, 1]],
    'S': [[0, 1, 1], [1, 1, 0]],
    'T': [[0, 1, 0], [1, 1, 1]],
    'Z': [[1, 1, 0], [0, 1, 1]]
}

def draw_shadow_text(stdscr, y, x, lines, color_pair, shadow_pair):
    for i, line in enumerate(lines):
        try:
            stdscr.addstr(y + i + 1, x + 1, line, curses.color_pair(shadow_pair))
            stdscr.addstr(y + i, x, line, curses.color_pair(color_pair) | curses.A_BOLD)
        except: pass

class Tetris:
    def __init__(self, h, w):
        self.h, self.w = h, w
        self.board = [[0]*w for _ in range(h)]
        self.score = 0
        self.new_piece()

    def new_piece(self):
        self.type = random.choice(list(SHAPES.keys()))
        self.shape = SHAPES[self.type]
        self.px = self.w // 2 - len(self.shape[0]) // 2
        self.py = 0
        return not self.collide(self.px, self.py)

    def collide(self, nx, ny, shape=None):
        if shape is None: shape = self.shape
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    if not (0 <= nx + x < self.w and 0 <= ny + y < self.h) or self.board[ny+y][nx+x]:
                        return True
        return False

    def rotate(self):
        ns = [list(r) for r in zip(*self.shape[::-1])]
        if not self.collide(self.px, self.py, ns): self.shape = ns

    def update(self):
        if not self.move(0, 1):
            for y, row in enumerate(self.shape):
                for x, cell in enumerate(row):
                    if cell: self.board[self.py+y][self.px+x] = 1
            nb = [r for r in self.board if not all(r)]
            cleared = self.h - len(nb)
            self.score += cleared * 100
            for _ in range(cleared): nb.insert(0, [0]*self.w)
            self.board = nb
            return self.new_piece()
        return True

    def move(self, dx, dy):
        if not self.collide(self.px + dx, self.py + dy):
            self.px += dx; self.py += dy
            return True
        return False

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(1000 // FPS)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)
    
    while True:
        sh, sw = stdscr.getmaxyx()
        tw, th = 10, 20
        game = Tetris(th, tw)
        last_fall = time.time()
        state = "PLAYING"

        while state == "PLAYING":
            key = stdscr.getch()
            if key in [ord('q'), ord('Q')]: return
            if key == curses.KEY_LEFT: game.move(-1, 0)
            if key == curses.KEY_RIGHT: game.move(1, 0)
            if key == curses.KEY_UP: game.rotate()
            if key == curses.KEY_DOWN: game.move(0, 1)
            if key == ord(' '):
                while game.move(0, 1): pass

            if time.time() - last_fall > max(0.1, 0.6 - (game.score/2000)):
                if not game.update(): state = "GAMEOVER"
                last_fall = time.time()

            stdscr.erase()
            logo_x = (sw - len(LOGO_MAIN[0])) // 2
            draw_shadow_text(stdscr, 1, logo_x, LOGO_MAIN, 1, 3)

            ox, oy = (sw - tw*2) // 2, (sh - th) // 2 + 3
            for y, r in enumerate(game.board):
                for x, c in enumerate(r):
                    if c: stdscr.addstr(oy+y, ox+x*2, BLOCK)
            for y, r in enumerate(game.shape):
                for x, c in enumerate(r):
                    if c: stdscr.addstr(oy+game.py+y, ox+(game.px+x)*2, BLOCK)
            
            stdscr.addstr(oy-1, ox-1, "┏"+"━"*(tw*2)+"┓")
            stdscr.addstr(oy+th, ox-1, "┗"+"━"*(tw*2)+"┛")
            stdscr.addstr(oy, ox+tw*2+4, f"SCORE: {game.score}")
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