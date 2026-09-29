# 🎮 Caro AI Game (20x20) - Pygame

Gomoku 20x20 game with AI. Game has 3 levels of AI from easy to hard.

---
## 🌟 Main function

- **Board size 20x20**.
- **Piece option:** Player can choose **X** or **O** (default: **X** always move first).
- **3 AI level:**
  - 🟢 **EASY (Random):** AI makes move randomly.
  - 🟡 **MEDIUM (Greedy):** AI can attack, blocking double-threat, 3-streak and 4-streak.
  - 🔴 **HARD (Pruning Alpha-Beta):** AI try many moves before bt Minimax associate with Alpha-Beta Pruning.
- **UX/UI:** Menu for pieces options and AI level, there are 3 shorcuts.

---

## 🛠️ System requirements & Setting

### Requirements
- **Python:** Version `3.8` or later.
- **Pip:** pip package.

### Steps

1. **Clone:**
   ```bash
   git clone https://github.com/AIEngineer992007/My-first-AI-project---Gomoku.git
   cd caro-ai-pygame
   ```

2. **Set up dependent libraries:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run:**
   ```bash
   python main_3.py / python3 main.py
   ```

---

## 🕹️ Tutorial

### using mouse
- **Menu:** Click choose piece and AI level.
- **In game:** Use left mouse to make move.

### (Hotkey)
| Key | Function |
| :---: | :--- |
| **`R`** | Reset Game |
| **`M`** | Back to Menu |
| **`Q`** | Quit game |
*Note*: 

---

## 🧠 Algorithm structure AI

- **Heuristic function (Evaluation Function):** Pattern Scoring such as *5-Streak, 4-Streak, Double-end,  4-streak blocked, 3-streak not blocked...* helps AI evaluates the optimistic move.
- **Alpha-Beta Pruning:** Iterating tree at depth=2, helps pruning not optimize branch and increase the speed of algorithm $20 \times 20$.
---
## Lisence