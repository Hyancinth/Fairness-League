# Fairness League

A webcam-based **Rock Paper Scissors** game where you play 21 rounds against **R.O.B.**, a robot opponent with a hidden AI strategy. The game uses real-time hand gesture recognition via your webcam.

*"How fair will you be?"*

---

## What It Does

Fairness League is a browser-based game built with Python/Flask that turns your webcam into a game controller. Point your hand at the camera to throw Rock, Paper, or Scissors — the app detects your gesture using [Google MediaPipe](https://ai.google.dev/edge/mediapipe/solutions/vision/hand_landmarker) hand landmarks and pits it against R.O.B.'s secretly chosen strategy.

The underlying research question: once you figure out the robot's pattern, will you exploit it?

---

## Features

- **Real-time gesture recognition** — hand detection runs asynchronously at ~120 ms per frame using MediaPipe
- **Three AI strategies** — R.O.B. secretly uses one of Random, Fixed, or Copycat play styles (see [How the AI Works](#how-the-ai-works))
- **21-round game** — ties don't increment the round counter
- **Animated robot face** — R.O.B. reacts emotionally (neutral → happy/ecstatic or sad/devastated) based on the score
- **Visual feedback** — bounding box overlay on the webcam feed shows detected hand
- **In-game rules modal** — tap the ⓘ button for gesture tips and game info

---

## Prerequisites

- **Python 3.12** (see `.python-version`)
- A **working webcam** connected to your machine
- A modern browser (Chrome/Edge/Firefox recommended)

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Hyancinth/Fairness-League.git
cd Fairness-League
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

> **Tip:** Use a virtual environment to keep dependencies isolated:
> ```bash
> python -m venv .venv
> source .venv/bin/activate   # Windows: .venv\Scripts\activate
> pip install -r requirements.txt
> ```

### 3. Run the server

```bash
python run.py
```

### 4. Open the game

Navigate to **http://127.0.0.1:5000** in your browser and grant webcam permissions when prompted.

---

## How to Play

1. Hold your hand clearly in front of the webcam — you'll see a bounding box appear when it's detected.
2. Click **Play Round** to start the 3-2-1 countdown.
3. At **GO!**, hold your gesture steady — the app captures your move and plays it against R.O.B.
4. The result, scores, and R.O.B.'s reaction are displayed immediately.
5. Play 21 rounds (ties excluded) to complete the game.

### Gesture reference

| Gesture | How to show it |
|---------|----------------|
| ✊ Rock | Closed fist |
| ✋ Paper | Open hand, all fingers extended |
| ✌️ Scissors | Index + middle finger extended — **tilt sideways** for best recognition |

---

## How the AI Works

R.O.B. uses a two-phase strategy:

| Phase | Rounds | Strategy |
|-------|--------|----------|
| Warmup | First 4 rounds | Random moves |
| Main | Rounds 5–21 | One of the three strategies below, chosen secretly at game start |

The three possible main strategies:

| Strategy | Behaviour |
|----------|-----------|
| **Random** | Picks Rock, Paper, or Scissors randomly each round |
| **Fixed** | Picks one move at game start and plays it every round |
| **Copycat** | Copies your previous move (first move is random) |

The player is never told which strategy is active — figuring it out (and deciding whether to exploit it) is part of the game.

---

## Project Structure

```
Fairness-League/
├── run.py                      # Entry point — creates and runs the Flask app
├── requirements.txt            # Python dependencies
├── .python-version             # Python 3.12.10
└── app/
    ├── __init__.py             # App factory
    ├── config.py               # Flask configuration
    ├── camera.py               # Webcam capture (OpenCV)
    ├── hand_landmark.py        # MediaPipe hand detection (async LIVE_STREAM mode)
    ├── gesture_classifier.py   # Landmark → Rock / Paper / Scissors
    ├── singletons.py           # Shared controller and camera instances
    ├── controller/
    │   └── controller.py       # Orchestrates frame capture → gesture → game
    ├── game/
    │   └── rps_game.py         # Game engine: rules, scoring, AI strategies
    ├── models/
    │   └── hand_landmarker.task  # MediaPipe hand landmark model (~7.5 MB)
    ├── blueprints/
    │   └── game_api/
    │       └── game_api.py     # REST API endpoints
    └── templates/
        └── index.html          # Game UI (single self-contained page)
```

---

## API Endpoints

The server exposes a small REST API under `/api`:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/frame` | GET | Returns the latest webcam frame (base64 JPEG) and detected gesture |
| `/api/play` | POST | Plays one round using the last detected gesture; returns round result and game state |
| `/api/reset` | POST | Resets the game to its initial state |

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Python 3.12 + Flask |
| Hand detection | Google MediaPipe (`hand_landmarker.task`) |
| Computer vision | OpenCV (`opencv-python`) |
| Numerical | NumPy |
| Frontend | Single-page HTML/CSS/JS (Jinja2 template) |

---

## Contributing

Contributions are welcome! Please open an issue or pull request on GitHub.

A few areas that would benefit from help:

- Additional AI strategies for R.O.B.
- Playtesting and balance feedback
- Accessibility improvements to the UI
- Unit tests for the game logic

---

## Support

- **Bug reports & feature requests:** [GitHub Issues](https://github.com/Hyancinth/Fairness-League/issues)
- **Project walkthrough & deep-dive:** [walkthrough.md](walkthrough.md)
