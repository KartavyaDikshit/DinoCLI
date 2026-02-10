"""
FROGGERCLI - 8-Bit Edition
Controls: [ARROWS] Move, [R] Restart, [Q] Quit
"""

import curses
import time
import random

FPS = 60
BLOCK = "██"
FROG = "▄█▄"
CAR = "████"

LOGO_MAIN = [
    r" ███████╗██████╗  ██████╗  ██████╗  ██████╗ ███████╗██████╗  ██████╗██╗     ██╗",
    r" ██╔════╝██╔══██╗██╔═══██╗██╔════╝ ██╔════╝ ██╔════╝██╔══██╗██╔════╝██║     ██║",
    r" █████╗  ██████╔╝██║   ██║██║  ███╗██║  ███╗█████╗  ██████╔╝██║     ██║     ██║",
    r" ██╔══╝  ██╔══██╗██║   ██║██║   ██║██║   ██║██╔══╝  ██╔══██╗██║     ██║     ██║",
    r" ██║     ██║  ██║╚██████╔╝╚██████╔╝╚██████╔╝███████╗██║  ██║╚██████╗███████╗██║",
    r" ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝╚══════╝╚═╝"
]

def draw_shadow_text(stdscr, y, x, lines, color_pair, shadow_pair):
    for i, line in enumerate(lines):
        try:
            stdscr.addstr(y + i + 1, x + 1, line, curses.color_pair(shadow_pair))
            stdscr.addstr(y + i, x, line, curses.color_pair(color_pair) | curses.A_BOLD)
        except: pass

class Frogger:
    def __init__(self, h, w):
        self.h, self.w = h, w
        self.reset_frog()
        self.level = 1
        self.lanes = []
        self.setup_lanes()
        self.score = 0
        self.dead = False
        self.won = False

    def reset_frog(self):
        self.fx, self.fy = self.w // 2, self.h - 2

    def setup_lanes(self):
        self.lanes = []
        for y in range(8, self.h - 3, 2):
            speed = random.uniform(0.1, 0.2 + (self.level * 0.05)) * random.choice([1, -1])
            self.lanes.append({
                'y': y,
                'speed': speed,
                'cars': [random.randint(0, self.w) for _ in range(3)]
            })

    def update(self, key):
        if key == curses.KEY_UP and self.fy > 7: 
            self.fy -= 1
            if self.fy == 7: # Goal reached
                self.score += 500
                self.level += 1
                self.reset_frog()
                self.setup_lanes()
                return

        if key == curses.KEY_DOWN and self.fy < self.h - 2: self.fy += 1
        if key == curses.KEY_LEFT and self.fx > 1: self.fx -= 2
        if key == curses.KEY_RIGHT and self.fx < self.w - 3: self.fx += 2

        for lane in self.lanes:
            for i in range(len(lane['cars'])):
                lane['cars'][i] += lane['speed']
                if lane['cars'][i] > self.w: lane['cars'][i] = -4
                if lane['cars'][i] < -4: lane['cars'][i] = self.w
                
                # Collision
                if int(lane['y']) == self.fy:
                    if lane['cars'][i] <= self.fx <= lane['cars'][i] + 4:
                        self.dead = True

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(1000 // FPS)
    curses.start_color()
    # Ensure colors exist
    try:
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
    except: pass

    while True:
        sh, sw = stdscr.getmaxyx()
        game = Frogger(sh, sw)
        
        while not game.dead:
            key = stdscr.getch()
            if key in [ord('q'), ord('Q')]: return
            game.update(key)

            stdscr.erase()
            logo_x = (sw - len(LOGO_MAIN[0])) // 2
            draw_shadow_text(stdscr, 1, logo_x, LOGO_MAIN, 1, 2)

            # Draw Start/Goal areas
            try:
                stdscr.addstr(7, 0, "█" * (sw - 1), curses.color_pair(3))
                stdscr.addstr(sh - 2, 0, "█" * (sw - 1), curses.color_pair(3))
            except: pass

            # Draw Lanes
            for lane in game.lanes:
                for car_x in lane['cars']:
                    if 0 <= int(car_x) < sw - 4:
                        try:
                            stdscr.addstr(lane['y'], int(car_x), CAR, curses.color_pair(4))
                        except: pass

            # Draw Frog
            try:
                stdscr.addstr(game.fy, game.fx, FROG, curses.color_pair(1) | curses.A_BOLD)
            except: pass

            try:
                stdscr.addstr(7, 2, f" SCORE: {game.score}   LEVEL: {game.level} ", curses.A_BOLD | curses.A_REVERSE)
            except: pass
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