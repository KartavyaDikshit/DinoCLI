"""
SNAKECLI - 8-Bit Edition
Controls: [ARROWS] Move, [R] Restart, [Q] Quit
"""

import curses
import time
import random

FPS = 15 # Snake is better at lower FPS for precision
BLOCK = "██"

LOGO_MAIN = [
    r" ███████╗███╗   ██╗ █████╗ ██╗  ██╗███████╗ ██████╗██╗     ██╗",
    r" ██╔════╝████╗  ██║██╔══██╗██║ ██╔╝██╔════╝██╔════╝██║     ██║",
    r" ███████╗██╔██╗ ██║███████║█████╔╝ █████╗  ██║     ██║     ██║",
    r" ╚════██║██║╚██╗██║██╔══██║██╔═██╗ ██╔══╝  ██║     ██║     ██║",
    r" ███████║██║ ╚████║██║  ██║██║  ██╗███████╗╚██████╗███████╗██║",
    r" ╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝ ╚═════╝╚══════╝╚═╝"
]

def draw_shadow_text(stdscr, y, x, lines, color_pair, shadow_pair):
    for i, line in enumerate(lines):
        try:
            stdscr.addstr(y + i + 1, x + 1, line, curses.color_pair(shadow_pair))
            stdscr.addstr(y + i, x, line, curses.color_pair(color_pair) | curses.A_BOLD)
        except: pass

class Snake:
    def __init__(self, h, w):
        self.h, self.w = h, w
        self.reset()

    def reset(self):
        self.snake = [[10, 10], [10, 9], [10, 8]]
        self.dir = curses.KEY_RIGHT
        self.food = self.spawn_food()
        self.score = 0
        self.dead = False

    def spawn_food(self):
        while True:
            f = [random.randint(8, self.h - 2), random.randint(1, self.w // 2 - 2)]
            if f not in self.snake: return f

    def update(self, key):
        if key in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]:
            # Prevent 180-degree turns - Wrapped in parentheses for safe line continuation
            if ((key == curses.KEY_UP and self.dir != curses.KEY_DOWN) or 
                (key == curses.KEY_DOWN and self.dir != curses.KEY_UP) or 
                (key == curses.KEY_LEFT and self.dir != curses.KEY_RIGHT) or 
                (key == curses.KEY_RIGHT and self.dir != curses.KEY_LEFT)):
                self.dir = key

        head = list(self.snake[0])
        if self.dir == curses.KEY_UP: head[0] -= 1
        elif self.dir == curses.KEY_DOWN: head[0] += 1
        elif self.dir == curses.KEY_LEFT: head[1] -= 1
        elif self.dir == curses.KEY_RIGHT: head[1] += 1

        # Death conditions
        if head[0] < 8 or head[0] >= self.h or head[1] < 0 or head[1] >= self.w // 2 or head in self.snake:
            self.dead = True
            return

        self.snake.insert(0, head)
        if head == self.food:
            self.score += 10
            self.food = self.spawn_food()
        else:
            self.snake.pop()

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(1000 // FPS)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)

    while True:
        sh, sw = stdscr.getmaxyx()
        game = Snake(sh - 1, sw)
        
        while not game.dead:
            key = stdscr.getch()
            if key in [ord('q'), ord('Q')]: return
            game.update(key)

            stdscr.erase()
            logo_x = (sw - len(LOGO_MAIN[0])) // 2
            draw_shadow_text(stdscr, 1, logo_x, LOGO_MAIN, 1, 2)

            # Draw Food
            stdscr.addstr(game.food[0], game.food[1] * 2, BLOCK, curses.color_pair(4))
            # Draw Snake
            for i, p in enumerate(game.snake):
                color = curses.color_pair(3) if i == 0 else curses.color_pair(1)
                stdscr.addstr(p[0], p[1] * 2, BLOCK, color)

            # Border
            for y in range(8, sh):
                stdscr.addstr(y, 0, "┃")
                stdscr.addstr(y, (sw // 2) * 2 - 1, "┃")
            stdscr.addstr(7, 0, "┏" + "━" * ((sw // 2) * 2 - 2) + "┓")
            stdscr.addstr(sh - 1, 0, "┗" + "━" * ((sw // 2) * 2 - 2) + "┛")
            
            stdscr.addstr(7, 5, f" SCORE: {game.score} ", curses.A_BOLD)
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