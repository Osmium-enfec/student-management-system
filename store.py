# store.py
import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DATA_FILE = os.path.join(DATA_DIR, "students.json")


def ensure_data_store():
    """Ensure data directory and JSON file exist."""
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f, indent=2)


def load_students():
    """Load students dict from JSON file."""
    ensure_data_store()
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}


def save_students(students):
    """Save students dict to JSON file."""
    ensure_data_store()
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(students, f, indent=2)
