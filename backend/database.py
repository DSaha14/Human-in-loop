import json
from pathlib import Path

DB_FILE = Path(__file__).parent / "data.json"

def load_data():
    if not DB_FILE.exists():
        with open(DB_FILE, "w") as f:
            json.dump({"requests": [], "knowledge": []}, f)
    with open(DB_FILE) as f:
        return json.load(f)

def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)
