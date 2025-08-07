import pandas as pd
from pathlib import Path

def load_data():
    input_path = Path("data/input/suricata_logs.csv")
    if input_path.exists():
        return pd.read_csv(input_path)
    return None
