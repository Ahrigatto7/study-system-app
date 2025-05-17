import pandas as pd
import os

PROGRESS_FILE = "data/progress.csv"

def update_progress(topic, percent):
    try:
        df = pd.read_csv(PROGRESS_FILE)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["topic", "completion"])
    if topic in df["topic"].values:
        df.loc[df["topic"] == topic, "completion"] = percent
    else:
        df = pd.concat([df, pd.DataFrame([{"topic": topic, "completion": percent}])], ignore_index=True)
    df.to_csv(PROGRESS_FILE, index=False)

def get_progress_report():
    if not os.path.exists(PROGRESS_FILE):
        return pd.DataFrame(columns=["topic", "completion"])
    return pd.read_csv(PROGRESS_FILE)