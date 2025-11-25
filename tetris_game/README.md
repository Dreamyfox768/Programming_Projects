# 🎮 TETRIS-CX

A modern implementation of **Tetris** built with Python, using **Turtle Graphics** for rendering and **Tkinter** for the GUI frontend.  
This project demonstrates modular architecture with separate backend and frontend layers.

---


---

## 🏗️ Architecture Overview

### Backend (Game Logic)
- **tetro_base.py** → `Cell` and `Tetromino` base classes (movement, rotation, collision detection).
- **etrominoes.py** → Implements all 7 Tetromino shapes (`O, I, S, Z, T, L, J`).
- **world.py** → Defines the `World` grid, manages spawning, line clearing, scoring, and game loop.

### Frontend (User Interface)
- **app.py** → Tkinter GUI (`TetrisApp`) with:
  - Play / Pause / Stop buttons
  - Score and Lines display
  - Embedded Turtle canvas
  - Keyboard controls (⬅ ➡ ⬆ ⬇ Space)

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- Tkinter (bundled with Python)
- Turtle (standard library)
- Math (sin, cos, pi)
- random (randint)


