"""
8-BIT PRO DINO RUN (main2.py)
----------------------------
Engine: Curses with optimized refresh
Characters: █, ▀, ▄, ▌ (Unicode Block Elements)
Controls: [SPACE/UP] Jump, [R] Restart, [Q] Quit
"""

import curses
import time
import random

# --- 8-BIT PIXEL ART (Refined Proportions) ---
# Dino is 6x12 pixels. Designed for a "chunky" 8-bit look.
DINO_RUN1 = [
    r"      ▄█████",
    r"      ██████",
    r"      ███▀▀▀",
    r"▄█████████  ",
    r"██████████  ",
    r"  █▄   █    "
]

DINO_RUN2 = [
    r"      ▄█████",
    r"      ██████",
    r"      ███▀▀▀",
    r"▄█████████  ",
    r"██████████  ",
    r"   █   █▄   "
]

DINO_JUMP = [
    r"      ▄█████",
    r"      ██████",
    r"      ███▀▀▀",
    r"▄█████████  ",
    r"██████████  ",
    r"  ▄█   ▄█   "
]

DINO_DEAD = [
    r"      ▄█████",
    r"      ███▀█▀",
    r"      ███▀▀▀",
    r"▄█████████  ",
    r"██████████  ",
    r"  █▄   █▄   "
]

# Cacti are shorter (4 lines) to ensure the jump clears them comfortably.
CACTUS = [
    r"  █  ",
    r"▄ █ ▄",
    r"█▀█▀█",
    r"  █  "
]

# --- ARCADE PHYSICS CONSTANTS (Fine-Tuned) ---
GRAVITY = 0.52          # Pull per frame
JUMP_FORCE = -3.2       # Initial burst (High enough to clear cacti)
MIN_JUMP_FORCE = -1.2   # For variable jump height logic
FPS = 60                # 60 FPS for ultra-smooth movement
MIN_WIDTH = 80
MIN_HEIGHT = 20

class ProDino:
    def __init__(self, x, ground_y):
        self.x = x
        self.ground_y = ground_y
        self.y = float(ground_y - 6)
        self.base_y = self.y
        self.vel_y = 0.0
        self.is_jumping = False
        self.frame_count = 0

    def jump(self):
        if not self.is_jumping:
            self.vel_y = JUMP_FORCE
            self.is_jumping = True

    def cut_jump(self):
        """Classic Arcade Mechanic: Shorten jump if button is released early."""
        if self.is_jumping and self.vel_y < MIN_JUMP_FORCE:
            self.vel_y = MIN_JUMP_FORCE

    def update(self):
        self.vel_y += GRAVITY
        self.y += self.vel_y

        # Floor collision
        if self.y >= self.base_y:
            self.y = self.base_y
            self.vel_y = 0
            self.is_jumping = False
        
        self.frame_count += 1

    def get_sprite(self, dead=False):
        if dead: return DINO_DEAD
        if self.is_jumping: return DINO_JUMP
        # Cycle legs every 6 frames at 60FPS
        return DINO_RUN1 if (self.frame_count // 6) % 2 == 0 else DINO_RUN2

class ProCactus:
    def __init__(self, x, ground_y):
        self.x = float(x)
        self.y = ground_y - 4
        self.width = 5
        self.height = 4

    def update(self, speed):
        self.x -= speed

def main(stdscr):
    # --- Curses Prep ---
    curses.curs_set(0)
    stdscr.nodelay(True)
    # Using small timeout to prevent blocking while maintaining FPS
    stdscr.timeout(1)
    
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Dino/Cactus
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK) # Score
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Ground
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)    # Game Over

    high_score = 0

    while True: # Outer loop for Restart
        sh, sw = stdscr.getmaxyx()
        if sh < MIN_HEIGHT or sw < MIN_WIDTH:
            stdscr.erase()
            stdscr.addstr(0, 0, "TERMINAL TOO SMALL! RE-SIZE TO 80x20")
            stdscr.refresh()
            time.sleep(1)
            continue

        ground_y = sh - 6
        dino = ProDino(12, ground_y)
        obstacles = []
        score = 0
        speed = 1.2
        spawn_timer = 0
        state = "PLAYING"
        space_pressed = False

        last_time = time.time()

        while state == "PLAYING":
            # --- Frame Timing (Locked 60 FPS) ---
            current_time = time.time()
            elapsed = current_time - last_time
            if elapsed < (1.0 / FPS):
                continue
            last_time = current_time

            # --- Input Handling ---
            key = stdscr.getch()
            if key in [ord(' '), curses.KEY_UP]:
                dino.jump()
                space_pressed = True
            elif key == -1 and space_pressed:
                # Key was released
                dino.cut_jump()
                space_pressed = False
            
            if key in [ord('q'), ord('Q')]: return

            # --- Logic ---
            dino.update()
            score += 0.15
            speed = min(3.5, 1.2 + (score / 400))
            
            spawn_timer -= 1
            if spawn_timer <= 0:
                obstacles.append(ProCactus(sw - 6, ground_y))
                spawn_timer = random.randint(30, 60)

            for obs in obstacles[:]:
                obs.update(speed)
                if obs.x < -6:
                    obstacles.remove(obs)
                
                # Collision Check
                dx, dy = int(dino.x), int(dino.y)
                ox, oy = int(obs.x), int(obs.y)
                # Tighter collision boxes for 8-bit feel
                if (dx + 2 < ox + 5 and dx + 9 > ox + 1 and 
                    dy + 1 < oy + 4 and dy + 5 > oy):
                    state = "DEAD"

            # --- Rendering ---
            stdscr.erase()
            
            # Draw Ground Line
            stdscr.addstr(ground_y + 1, 0, "█" * (sw - 1), curses.color_pair(3))
            
            # Draw Obstacles
            for obs in obstacles:
                for i, line in enumerate(CACTUS):
                    if 0 <= int(obs.x) < sw - 6:
                        stdscr.addstr(int(obs.y) + i, int(obs.x), line, curses.color_pair(1))
            
            # Draw Dino
            sprite = dino.get_sprite()
            for i, line in enumerate(sprite):
                if 0 <= int(dino.x) < sw - 12:
                    stdscr.addstr(int(dino.y) + i, int(dino.x), line, curses.color_pair(1))
            
            # Scoreboard
            high_score = max(high_score, int(score))
            stdscr.addstr(1, sw - 22, f"HI-SCORE: {high_score:05}", curses.color_pair(2) | curses.A_BOLD)
            stdscr.addstr(2, sw - 22, f"SCORE:    {int(score):05}", curses.color_pair(2))
            
            stdscr.refresh()

        # --- Game Over Screen ---
        sprite = dino.get_sprite(dead=True)
        for i, line in enumerate(sprite):
            stdscr.addstr(int(dino.y) + i, int(dino.x), line, curses.color_pair(4))
        
        msg = "  █▀▀ █▀█ █▀▄▀█ █▀▀   █▀█ █░█ █▀▀ █▀█  "
        msg2 = "  █▄█ █▀█ █░▀░█ ██▄   █▄█ ▀▄▀ ██▄ █▀▄  "
        stdscr.addstr(sh // 2 - 1, (sw - len(msg)) // 2, msg, curses.color_pair(4))
        stdscr.addstr(sh // 2, (sw - len(msg2)) // 2, msg2, curses.color_pair(4))
        stdscr.addstr(sh // 2 + 2, (sw - 18) // 2, "PRESS 'R' TO RETRY", curses.A_BOLD)
        stdscr.refresh()

        while True:
            key = stdscr.getch()
            if key in [ord('r'), ord('R')]: break
            if key in [ord('q'), ord('Q')]: return

if __name__ == "__main__":
    curses.wrapper(main)
