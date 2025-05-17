
# OSRS Loot Simulator

This is a Flask-based web simulator for OSRS-style boss loot drops. It supports three custom bosses: Blood Moon, Blue Moon, and Eclipse Moon. The app simulates kill counts (KC), rolls for unique and common loot, and streams results in real time using Server-Sent Events (SSE).

## Features

- Simulates unique item drops with accurate drop rates
- Rolls for standard loot based on rarity and quantity ranges
- Tracks total loot value and item counts
- Streams data live to the frontend per KC
- Custom loot tables per boss with reset behavior

## Tech Stack

- Python 3, Flask, Jinja2
- HTML/CSS (simple frontend)
- Server-Sent Events for real-time output
- Flask-CORS for cross-origin requests

## Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

```bash
git clone https://github.com/aliozertekin/osrs-loot-simulator.git
cd osrs-loot-simulator
pip install -r requirements.txt
python app.py
```

Visit `http://localhost:5000` in your browser.

## API

### `/simulate`

Supports both GET and POST requests.

- `kc_count`: number of kills to simulate (default: 105)
- `bosses`: comma-separated list or array of selected bosses

Returns a real-time event stream of loot updates per kill.

Example GET:
```
/simulate?kc_count=150&bosses=Blood%20Moon,Blue%20Moon
```

## Customization

To add or change loot tables, edit:
- `unique_items` and `standard_loot` in `app.py`
- `unique_items_pool` logic in `/simulate`

## License

MIT
