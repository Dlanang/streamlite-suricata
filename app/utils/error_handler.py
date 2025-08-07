# app/utils/error_handler.py
import traceback
from datetime import datetime
import os

ERROR_LOG = "logs/error.log"

def log_error(err: Exception, context: str = "N/A"):
    os.makedirs(os.path.dirname(ERROR_LOG), exist_ok=True)

    with open(ERROR_LOG, "a", encoding="utf-8") as f:
        f.write(f"\n--- {datetime.utcnow().isoformat()} ---\n")
        f.write(f"[Context] {context}\n")
        f.write(f"[Error] {str(err)}\n")
        f.write(traceback.format_exc())
        f.write("\n")

