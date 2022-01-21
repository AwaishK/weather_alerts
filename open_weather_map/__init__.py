from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.joinpath("DATA")

if not DATA_DIR.is_dir():
    try:
        DATA_DIR.mkdir()
    except Exception as e:
        print(e)
