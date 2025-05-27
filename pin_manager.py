import hashlib
import os
import json

PIN_FILE = "pin_config.json"

def hash_pin(pin):
    return hashlib.sha256(pin.encode()).hexdigest()

def pin_exists():
    return os.path.exists(PIN_FILE)

def set_pin(new_pin):
    with open(PIN_FILE, "w") as f:
        json.dump({"pin_hash": hash_pin(new_pin)}, f)

def validate_pin(entered_pin):
    if not pin_exists():
        return False
    with open(PIN_FILE, "r") as f:
        data = json.load(f)
        return data["pin_hash"] == hash_pin(entered_pin)
