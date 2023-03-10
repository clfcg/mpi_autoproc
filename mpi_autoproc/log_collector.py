from pathlib import Path
from datetime import datetime


def create_logfile():
    log_file = Path(__file__).resolve().parent / "logs.log"
    if not Path(log_file).is_file():
        Path(log_file).touch()
    return log_file

def get_log(inp_text: str):
    log_file = create_logfile()
    log_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"{log_datetime} >\t{inp_text}\n")
    print(f"{log_datetime} >\t{inp_text}\n")
