"""
DinoCLI - 8-Bit Deluxe Edition
Run with: python dino.py

Controls:
- SPACE / UP: Jump
- R: Restart
- Q: Quit
"""

import curses
import time
import random

# --- 8-BIT BLOCKY LOGO (Shadowed) ---
LOGO_MAIN = [
    r" ██████╗ ██╗███╗   ██╗ ██████╗  ██████╗██╗     ██╗",
    r" ██╔══██╗██║████╗  ██║██╔═══██╗██╔════╝██║     ██║",
    r" ██║  ██║██║██╔██╗ ██║██║   ██║██║     ██║     ██║",
    r" ██║  ██║██║██║╚██╗██║██║   ██║██║     ██║     ██║",
    r" ██████╔╝██║██║ ╚████║╚██████╔╝╚██████╗███████╗██║",
    r" ╚═════╝ ╚═╝╚═╝  ╚═══╝ ╚═════╝  ╚═════╝╚══════╝╚═╝"
]

# --- 8-BIT SPRITES ---
DINO_RUN1 = [
    r"      ███████",
    r"      ███ ███",
    r"      ███████",
    r"███████████  ",
    r"███████████  ",
    r"  ███   ███  "
]

DINO_RUN2 = [
    r"      ███████",
    r"      ███ ███",
    r"      ███████",
    r"███████████  ",
    r"███████████  ",
    r"    ███   ███"
]

DINO_JUMP = [
    r"      ███████",
    r"      ███ ███",
    r"      ███████",
    r"███████████  ",
    r"███████████  ",
    r"  █████████  "
]

DINO_DEAD = [
    r"      ███████",
    r"      ███X███",
    r"      ███████",
    r"███████████  ",
    r"███████████  ",
    r"  ███   ███  "
]

CACTUS = [
    r"  ███  ",
    r"  ███  ",
    r"███████",
    r"  ███  ",
    r"  ███  ",
    r"  ███  "
]

# --- Constants ---
GRAVITY = 0.6
JUMP_STRENGTH = -3.8
FPS = 45 
MIN_WIDTH = 85
MIN_HEIGHT = 26

class Dino:
    def __init__(self, x, ground_y):
        self.x = x
        self.ground_y = ground_y
        self.y = float(ground_y - 6)
        self.base_y = self.y
        self.velocity = 0.0
        self.is_jumping = False
        self.frame = 0

    def jump(self):
        if not self.is_jumping:
            self.velocity = JUMP_STRENGTH
            self.is_jumping = True

    def update(self):
        if self.is_jumping:
            self.velocity += GRAVITY
            self.y += self.velocity
            if self.y >= self.base_y:
                self.y = self.base_y
                self.velocity = 0
                self.is_jumping = False
        self.frame = (self.frame + 1) % 12

    def get_sprite(self, dead=False):
        if dead: return DINO_DEAD
        if self.is_jumping: return DINO_JUMP
        return DINO_RUN1 if self.frame < 6 else DINO_RUN2

class Obstacle:
    def __init__(self, x, ground_y):
        self.sprite = CACTUS
        self.width = len(self.sprite[0])
        self.height = len(self.sprite)
        self.x = float(x)
        self.y = float(ground_y - self.height + 1)

    def update(self, speed):
        self.x -= speed

def draw_shadow_text(stdscr, y, x, lines, color_pair, shadow_pair):
    """Draws text with a drop-shadow effect."""
    for i, line in enumerate(lines):
        # Draw shadow first (offset by 1,1)
        try:
            stdscr.addstr(y + i + 1, x + 1, line, curses.color_pair(shadow_pair))
        except: pass
        # Draw main text
        try:
            stdscr.addstr(y + i, x, line, curses.color_pair(color_pair) | curses.A_BOLD)
        except: pass

def main(stdscr):
    # Setup Colors
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(1000 // FPS)
    
    curses.start_color()
    # Color Pairs: (ID, Foreground, Background)
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Text
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_BLACK)  # Dummy/Shadow helper
    # Some terminals don't support custom colors well, so we use defaults
    curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)   # Shadow color
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Dino
    curses.init_pair(5, curses.COLOR_RED, curses.COLOR_BLACK)    # Game Over Shadow

    high_score = 0

    while True:
        sh, sw = stdscr.getmaxyx()
        if sh < MIN_HEIGHT or sw < MIN_WIDTH:
            stdscr.erase()
            stdscr.addstr(0, 0, f"Resize terminal: {sw}/{MIN_WIDTH} x {sh}/{MIN_HEIGHT}")
            stdscr.refresh()
            time.sleep(1)
            continue

        ground_y = sh - 6
        dino = Dino(12, ground_y)
        obstacles = []
        score = 0
        speed = 1.2
        spawn_timer = 0
        state = "PLAYING"

        while state == "PLAYING":
            key = stdscr.getch()
            if key in [ord('q'), ord('Q')]: return
            if key in [ord(' '), curses.KEY_UP]: dino.jump()

            dino.update()
            score += 0.1
            speed = min(3.0, 1.2 + (score / 500))
            
            spawn_timer -= 1
            if spawn_timer <= 0:
                obstacles.append(Obstacle(sw - 8, ground_y))
                spawn_timer = random.randint(35, 70)

            for obs in obstacles[:]:
                obs.update(speed)
                if obs.x < -8: obstacles.remove(obs)
                # Collision Logic
                dx, dy = int(dino.x) + 2, int(dino.y)
                if (dx < obs.x + obs.width and dx + 10 > obs.x and 
                    dy < obs.y + obs.height and dy + 6 > obs.y):
                    state = "DEAD"

            stdscr.erase()
            
            # --- Draw Header with Shadow ---
            draw_shadow_text(stdscr, 1, (sw - len(LOGO_MAIN[0])) // 2, LOGO_MAIN, 1, 3)
            
            # --- Draw Ground ---
            stdscr.addstr(ground_y + 1, 0, "█" * (sw - 1), curses.color_pair(1))
            
            # --- Draw Obstacles ---
            for obs in obstacles:
                for i, line in enumerate(obs.sprite):
                    if 0 <= int(obs.x) < sw - len(line):
                        stdscr.addstr(int(obs.y) + i, int(obs.x), line, curses.color_pair(4))
            
            # --- Draw Dino ---
            sprite = dino.get_sprite()
            for i, line in enumerate(sprite):
                if 0 <= int(dino.x) < sw - len(line):
                    stdscr.addstr(int(dino.y) + i, int(dino.x), line, curses.color_pair(4))
                
            # --- Draw HUD ---
            high_score = max(high_score, int(score))
            hud = f" 🏆 SCORE: {int(score):05}   HI: {high_score:05} "
            stdscr.addstr(sh - 2, (sw - len(hud)) // 2, hud, curses.A_REVERSE | curses.A_BOLD)
            
            stdscr.refresh()

        # --- Game Over Screen ---
        stdscr.attron(curses.A_BOLD)
        go_lines = [
            r"  ▄████  ▄▄▄       ███▄ ▄███▓▓█████     ▒█████   ██▒   █▓▓█████  ██▀███  ",
            r" ██▒ ▀█▒▒████▄    ▓██▒▀█▀ ██▒▓█   ▀    ▒██▒  ██▒▓██░   █▒▓█   ▀ ▓██ ▒ ██▒",
            r"▒██░▄▄▄░▒██  ▀█▄  ▓██    ▓██░▒███      ▒██░  ██▒ ▓██  █▒░▒███   ▓██ ░▄█ ▒",
            r"░▓█  ██▓░██▄▄▄▄██ ▒██    ▒██ ▒▓█  ▄    ▒██   ██░  ▒██ █░░▒▓█  ▄ ▒██▀▀█▄  ",
            r"░▒▓███▀▒ ▓█   ▓██▒▒██▒   ░██▒░▒████▒   ░ ████▓▒░   ▒▀█░  ░▒████▒░██▓ ▒██▒",
            r" ░▒   ▒  ▒▒   ▓▒█░░ ▒░   ░  ░░░ ▒░ ░   ░ ▒░▒░▒░    ░ ▐░  ░░ ▒░ ░░ ▒▓ ░▒▓░",
            r"  ░   ░   ▒   ▒▒ ░░  ░      ░ ░ ░  ░     ░ ▒ ▒░    ░ ░░   ░ ░  ░  ░▒ ░ ▒░",
            r"░ ░   ░   ░   ▒   ░      ░      ░        ░ ░ ░ ▒       ░░     ░     ░░   ░ ",
            r"      ░       ░  ░       ░      ░  ░         ░ ░        ░     ░  ░   ░     "
        ]
        
        draw_shadow_text(stdscr, sh // 2 - 5, (sw - len(go_lines[0])) // 2, go_lines, 1, 5)
        
        retry = "PRESS 'R' TO RESTART OR 'Q' TO QUIT"
        stdscr.addstr(sh // 2 + 6, (sw - len(retry)) // 2, retry, curses.A_BOLD)
        stdscr.refresh()

        while True:
            key = stdscr.getch()
            if key in [ord('r'), ord('R')]: break
            if key in [ord('q'), ord('Q')]: return

if __name__ == "__main__":
    curses.wrapper(main)
