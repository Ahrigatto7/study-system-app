import pandas as pd
import os
from datetime import datetime

NOTE_FILE = "data/notes.csv"

def save_note(title, content, tags, filename=None, category="General"):
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df = pd.DataFrame([{
        "title": title,
        "content": content,
        "tags": tags,
        "filename": filename if filename else "",
        "category": category,
        "created_at": created_at
    }])
    if os.path.exists(NOTE_FILE):
        df.to_csv(NOTE_FILE, mode="a", header=False, index=False)
    else:
        df.to_csv(NOTE_FILE, index=False)

def load_notes():
    if not os.path.exists(NOTE_FILE):
        return pd.DataFrame(columns=["title", "content", "tags", "filename", "category", "created_at"])
    return pd.read_csv(NOTE_FILE)