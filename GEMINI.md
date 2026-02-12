# DinoCLI - 8-Bit Retro Arcade Suite

## Project Overview
DinoCLI is a collection of high-fidelity, terminal-based recreations of classic arcade games. The project emphasizes a consistent "8-bit deluxe" aesthetic, utilizing Unicode block elements and drop-shadow effects to simulate pixel art within a command-line interface.

### Main Technologies
- **Language:** Python 3.x
- **Graphics & Input:** `curses` (standard library on Linux/macOS, requires `windows-curses` package on Windows)
- **Process Management:** `subprocess` (used by the arcade launcher to manage game transitions)

### Architecture
- **Arcade Launcher (`arcade.py`):** The central hub providing an interactive menu to select and launch individual games. It manages terminal state transitions between the menu and subprocesses.
- **Game Modules:** Each game is a self-contained Python script implementing its own engine, physics, and rendering logic:
    - `dino2.py`: A Chrome Dino clone with refined arcade physics and speed scaling.
    - `tetris.py`: A full-featured Tetris implementation with rotation logic and line clearing.
    - `invaders.py`: A Space Invaders clone with alien horde movement and projectile logic.
    - `pong.py`: A classic Pong implementation with AI and player controls.
- **Visual Style:** All games share a unified rendering pattern using `█`, `▀`, `▄`, and `▌` characters, 60 FPS frame-rate limiting, and layered drop-shadow headers.

---

## Building and Running

### Prerequisites
- Python 3.8 or higher.
- **Linux/macOS:** No additional dependencies required.
- **Windows Users:** Must install the curses support package:
  ```bash
  pip install windows-curses
  ```

### Running the Arcade
To start the central menu and access all games:
```bash
python arcade.py
```

### Running Individual Games
You can also launch any game directly:
```bash
python dino2.py
python tetris.py
python invaders.py
python pong.py
```

---

## Development Conventions

### Visual Standards
- **Pixel Art:** Use Unicode Block Elements (█, ▀, ▄, ▌) instead of standard ASCII characters for all game entities.
- **Strict No-Emoji Mandate:** Emojis are strictly prohibited in all project files, including code, HUDs, menus, and documentation (README, etc.). Maintain a pure 8-bit aesthetic using only text and block characters.
- **Shadow Headers:** Use the draw_shadow_text function for consistent, high-impact titles with Cyan or Red shadows.

### Coding Practices
- **Performance:** Use `stdscr.timeout()` and `time.sleep()` to lock gameplay to a stable 60 FPS.
- **Safety:** Always wrap the `main` function with `curses.wrapper(main)` to ensure terminal settings (echo, cursor visibility) are restored even if the script crashes.
- **Controls:** Standardize input where possible:
    - `SPACE` / `UP`: Jump or Primary Action.
    - `ARROWS`: Navigation/Movement.
    - `R`: Restart game after Game Over.
    - `Q`: Quit game or return to menu.
- **Hitboxes:** Implement "Arcade Physics" with tightened hitboxes (using pixel-based character offsets) to ensure fair and responsive gameplay.
