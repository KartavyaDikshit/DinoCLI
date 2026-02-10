"""
RETRO ARCADE LAUNCHER - 8-Bit Edition
Run with: python arcade.py

Controls:
- ARROWS: Navigate
- ENTER: Play Game
- Q: Exit Arcade
"""

import curses
import subprocess
import os
import time

# --- 8-BIT ARCADE HEADER ---
ARCADE_LOGO = [
    r" █████╗ ██████╗  ██████╗  █████╗ ██████╗ ███████╗",
    r"██╔══██╗██╔══██╗██╔════╝ ██╔══██╗██╔══██╗██╔════╝",
    r"███████║██████╔╝██║      ███████║██║  ██║█████╗  ",
    r"██╔══██║██╔══██╗██║      ██╔══██║██║  ██║██╔══╝  ",
    r"██║  ██║██║  ██║╚██████╗ ██║  ██║██████╔╝███████╗",
    r"╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚══════╝"
]

GAMES = [
    {"name": "DINO RUN PRO", "file": "dino2.py"},
    {"name": "TETRIS BLOCK", "file": "tetris.py"},
    {"name": "SPACE INVADERS", "file": "invaders.py"},
    {"name": "PONG CLASSIC", "file": "pong.py"},
    {"name": "SNAKE PRO", "file": "snake.py"},
    {"name": "BREAKOUT BRICK", "file": "breakout.py"},
    {"name": "FROGGER CROSS", "file": "frogger.py"}
]

def draw_shadow_text(stdscr, y, x, lines, color_pair, shadow_pair):
    for i, line in enumerate(lines):
        try:
            stdscr.addstr(y + i + 1, x + 1, line, curses.color_pair(shadow_pair))
            stdscr.addstr(y + i, x, line, curses.color_pair(color_pair) | curses.A_BOLD)
        except: pass

def main(stdscr):
    # Setup Colors
    curses.curs_set(0)
    stdscr.nodelay(False) 
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)  
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)   
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)  
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK) 

    current_row = 0

    while True:
        sh, sw = stdscr.getmaxyx()
        stdscr.erase()

        # --- Draw Logo ---
        logo_x = (sw - len(ARCADE_LOGO[0])) // 2
        draw_shadow_text(stdscr, 2, logo_x, ARCADE_LOGO, 1, 2)

        # --- Draw Menu ---
        menu_y = 10
        for idx, game in enumerate(GAMES):
            x = (sw - 30) // 2
            y = menu_y + (idx * 3)
            
            if idx == current_row:
                stdscr.attron(curses.color_pair(3) | curses.A_BOLD)
                stdscr.addstr(y, x, f" > [ {game['name']} ] < ")
                stdscr.attroff(curses.color_pair(3) | curses.A_BOLD)
            else:
                stdscr.addstr(y, x, f"   {game['name']}   ", curses.color_pair(4))

        # --- Footer ---
        footer = "USE ARROWS TO NAVIGATE • ENTER TO PLAY • Q TO EXIT"
        stdscr.addstr(sh - 3, (sw - len(footer)) // 2, footer, curses.A_DIM)

        stdscr.refresh()

        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(GAMES) - 1:
            current_row += 1
        elif key in [ord('\n'), curses.KEY_ENTER, 10, 13]:
            # Launch Game
            game_file = GAMES[current_row]['file']
            if os.path.exists(game_file):
                # Properly exit curses mode before launching subprocess
                curses.endwin()
                
                # Execute the game as a separate process
                # Using 'python' as identified previously as the working command
                subprocess.run(["python", game_file])
                
                # Re-initialize the terminal/screen after game exits
                stdscr.clear()
                stdscr.refresh()
            else:
                stdscr.addstr(sh-2, (sw-20)//2, f"FILE {game_file} NOT FOUND!", curses.color_pair(2))
                stdscr.refresh()
                time.sleep(1)
        elif key in [ord('q'), ord('Q')]:
            break

if __name__ == "__main__":
    curses.wrapper(main)