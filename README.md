# DinoCLI - 8-Bit Deluxe Arcade

```text
 ██████╗ ██╗███╗   ██╗  ██████╗  ██████╗██╗     ██╗
 ██╔══██╗██║████╗  ██║ ██╔═══██╗██╔════╝██║     ██║
 ██║  ██║██║██╔██╗ ██║ ██║   ██║██║     ██║     ██║
 ██║  ██║██║██║╚██╗██║ ██║   ██║██║     ██║     ██║
 ██████╔╝██║██║ ╚████║ ╚██████╔╝╚██████╗███████╗██║
 ╚═════╝ ╚═╝╚═╝  ╚═══╝  ╚═════╝  ╚═════╝╚══════╝╚═╝
```

Python-based 8-bit arcade suite for the terminal.

A high-performance, terminal-based arcade suite featuring 8-bit recreations of classic games. Built entirely in Python using the curses module, this collection features a bold 8-bit aesthetic, Unicode block-element sprites, and layered drop-shadow visual effects.

---

## Included Games

The suite currently features 7 classic arcade recreations:

1.  Dino Run Pro (dino2.py): The definitive terminal dino experience with arcade physics.
2.  Tetris Block (tetris.py): Full-featured Tetris with rotation and line clearing.
3.  Space Invaders (invaders.py): Defend Earth from waves of 8-bit aliens.
4.  Pong Classic (pong.py): Smooth, fast-paced table tennis for two players.
5.  Snake Pro (snake.py): High-precision snake growth and survival.
6.  Breakout Brick (breakout.py): Shatter colorful brick walls with arcade physics.
7.  Frogger Cross (frogger.py): Dodge traffic and level up by reaching the goal.

---

## Signature 8-Bit Style

- Unicode Block Graphics: Every sprite is designed using █, ▀, ▄, and ▌ characters to simulate authentic retro pixels.
- Arcade Refresh Rate: Locked 60 FPS (15 FPS for Snake) ensures zero flickering and buttery smooth movement.
- Drop Shadow HUDs: High-impact headers with Cyan and Red shadows for that premium Deluxe feel.
- Variable Physics: Snappy jumping, acceleration, and collision detection tuned for terminal responsiveness.
- Pure Text Aesthetic: No emojis allowed. Strictly block art and text.

---

## Global Controls

| Key | Action |
| :--- | :--- |
| ARROWS | Movement / Navigation |
| SPACE | Jump / Shoot / Action |
| ENTER | Select Game (in Arcade) |
| R | Restart (after Game Over) |
| Q | Quit / Back to Menu |

---

## Installation and Running

### 1. Clone the repository
```bash
git clone https://github.com/KartavyaDikshit/DinoCLI.git
cd DinoCLI
```

### 2. Install Dependencies
The game uses the standard curses library. On Windows, you will need the support package:
```bash
pip install windows-curses
```

### 3. Launch the Arcade
Ensure your terminal is expanded (recommended 100x30) for the best visual experience:
```bash
python arcade.py
```

---

## Technical Details

- Rendering: Optimized curses loops with stdscr.timeout() for frame-rate limiting.
- Launcher: arcade.py manages terminal states and subprocess execution for seamless game transitions.
- Hitboxes: Pixel-perfect bounding box collision logic implemented in character space.

---

## License

Distributed under the MIT License. See LICENSE for more information.

---

**Insert Coin to Begin!**
