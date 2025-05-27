from datetime import datetime

LOG_FILE = "activity.log"

def log_action(action, details=""):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {action}: {details}\n"
    with open(LOG_FILE, "a") as f:
        f.write(entry)
