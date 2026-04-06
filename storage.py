import json
import os
from datetime import date

DATA_DIR       = 'data'
FAVOURITES_FILE = os.path.join(DATA_DIR, 'favourites.json')
MASTERY_FILE    = os.path.join(DATA_DIR, 'mastery.json')

os.makedirs(DATA_DIR, exist_ok=True)

# ── Favourites ──────────────────────────────────────────────

def load_favourites() -> set:
    if not os.path.exists(FAVOURITES_FILE):
        return set()
    with open(FAVOURITES_FILE, 'r') as f:
        return set(json.load(f))

def save_favourites(favs: set) -> None:
    with open(FAVOURITES_FILE, 'w') as f:
        json.dump(sorted(favs), f)

def toggle_favourite(char: str) -> bool:
    """Toggle char in favourites. Returns True if now favourited."""
    char = char.upper()
    favs = load_favourites()
    if char in favs:
        favs.remove(char)
    else:
        favs.add(char)
    save_favourites(favs)
    return char in favs

# ── Mastery ──────────────────────────────────────────────────

def load_mastery() -> dict:
    if not os.path.exists(MASTERY_FILE):
        return {}
    with open(MASTERY_FILE, 'r') as f:
        return json.load(f)

def save_mastery(data: dict) -> None:
    with open(MASTERY_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def update_mastery(char: str, correct: bool) -> None:
    """Record an attempt for a character."""
    char = char.upper()
    data = load_mastery()
    if char not in data:
        data[char] = {'attempts': 0, 'correct': 0, 'last_seen': None}
    data[char]['attempts'] += 1
    if correct:
        data[char]['correct'] += 1
    data[char]['last_seen'] = date.today().isoformat()
    save_mastery(data)

def get_mastery_level(char_data: dict) -> str:
    """Return 'unseen', 'learning', or 'mastered' from a char's data dict."""
    attempts = char_data.get('attempts', 0)
    correct  = char_data.get('correct', 0)
    if attempts == 0:
        return 'unseen'
    accuracy = correct / attempts
    if attempts >= 10 and accuracy >= 0.80:
        return 'mastered'
    return 'learning'

def get_mastery_level_for(char: str) -> str:
    """Convenience wrapper — looks up char in mastery file directly."""
    data = load_mastery()
    return get_mastery_level(data.get(char.upper(), {}))