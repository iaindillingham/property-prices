from pathlib import Path

__version__ = "0.1.0"

ROOT_DIR = Path(__file__).parents[1]

DATA_DIR = ROOT_DIR / "data"
EXTERNAL_DIR = DATA_DIR / "external"
RAW_DIR = DATA_DIR / "raw"
INTERIM_DIR = DATA_DIR / "interim"
PROCESSED_DIR = DATA_DIR / "processed"
