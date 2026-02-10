# 🦖 DinoCLI - 8-Bit Deluxe Edition

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A high-performance, terminal-based recreation of the classic Google Chrome "No Internet" Dinosaur Game. Built entirely in Python using the `curses` module, this version features a bold 8-bit aesthetic, smooth animations, and retro visual effects.

---

## ✨ Features

- **8-Bit Retro Graphics:** Custom-designed blocky ASCII art for the Dino, obstacles, and terrain.
- **Dynamic Physics:** Gravity-based jumping logic with acceleration and velocity for a natural feel.
- **Visual Effects:** 
  - **Drop Shadows:** Layered 3D text effects for the logo and Game Over screens.
  - **Parallax Background:** Scrolling terrain markers to simulate speed.
- **Difficulty Scaling:** The game speed and spawn frequency increase as your score gets higher.
- **High Score Tracking:** Keep track of your best run during each session.
- **Cross-Platform Support:** Optimized for Linux, macOS, and Windows.

---

## 🎮 Controls

| Key | Action |
| :--- | :--- |
| `SPACE` or `UP` | **Jump** |
| `R` | **Restart** (after Game Over) |
| `Q` | **Quit** |

---

## 🚀 Installation & Running

### 1. Clone the repository
```bash
git clone https://github.com/KartavyaDikshit/DinoCLI.git
cd DinoCLI
```

### 2. Install Dependencies
The game uses the standard `curses` library. On **Windows**, you'll need to install the support package:
```bash
pip install windows-curses
```

### 3. Play the Game
Ensure your terminal is expanded to at least **85x26** for the best visual experience:
```bash
python dino.py
```

---

## 🛠️ Technical Details

- **Rendering Engine:** Built on the Python `curses` module for flicker-free, non-blocking terminal input and output.
- **Hitbox Logic:** Pixel-perfect (character-based) collision detection with tightened bounding boxes for fair gameplay.
- **Game Loop:** A robust 45 FPS loop ensures smooth character movement and responsive controls.

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

---

**Happy Jumping!** 🦖💨
