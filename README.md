# Popper Fish

Popper Fish is a small arcade-style underwater shooter built with Python and Pygame. You control a yellow submarine, dodge incoming fish, shoot bubbles, collect powerups, and try to survive long enough to earn a high score.

## Requirements

- Python 3.12 or newer
- pip
- Pygame dependency from `requirements.txt`

The project supports Python 3.14 by using `pygame-ce`, because standard `pygame` may not have a prebuilt wheel for Python 3.14 on Windows.

## Install

From the project folder:

```powershell
cd "C:\Users\ASUS i5 13thGen\Desktop\Tammy\PROJECT\popperFish\popper-fish"
py -m pip install -r requirements.txt
```

If your machine uses `python` instead of `py`, you can use:

```powershell
python -m pip install -r requirements.txt
```

## Run

From the project folder:

```powershell
py main.py
```

or:

```powershell
python main.py
```

The top-level `main.py` is the launcher. It starts the organized code in `src/main.py`.

## How To Play

- Move left and right to avoid fish.
- Shoot bubbles upward to pop fish.
- Survive as long as possible.
- Collect powerups:
  - Pearl and shell increase attack power.
  - Seaweed and algae restore health.
- If your health reaches zero, the game shows the leaderboard screen.

Default controls:

```text
A       Move left
D       Move right
Space   Shoot
```

The start/menu screen includes Settings, where you can change the movement/shoot keys and adjust music volume.


## Project Structure

```text
main.py                  Launcher
requirements.txt         Python dependencies
highscore.txt            Existing score data file
assets/                  Images and sounds
src/main.py              Main app flow and screens
src/game/constants.py    Game constants and asset paths
src/game/game_state.py   Gameplay loop, spawning, movement, collisions
src/game/ui.py           Drawing, buttons, HUD, menus, leaderboard
src/entities/            Fish and powerup classes
src/utils/helpers.py     Asset loading and audio helpers
```


