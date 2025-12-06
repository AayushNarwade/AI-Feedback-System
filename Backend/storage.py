import json
import os

DATA_FILE = "data.json"


def initialize_file():
    """Ensures the JSON file exists and contains a valid empty list."""
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump([], f)
        return

    # If file exists but empty, write empty list
    if os.path.getsize(DATA_FILE) == 0:
        with open(DATA_FILE, "w") as f:
            json.dump([], f)


def load_data():
    """Loads submissions safely."""
    initialize_file()

    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_data(data):
    """Saves the entire list back to the file."""
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)
