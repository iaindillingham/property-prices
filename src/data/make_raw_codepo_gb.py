"""Reads external and writes raw Ordnance Survey Code-Point Open CSVs.

External CSVs are split by postcode area and do not have header rows.
The raw CSV has a header row.
"""
import csv

from src import EXTERNAL_DIR, RAW_DIR

EXTERNAL_CODEPO_GB_DIR = EXTERNAL_DIR / "codepo_gb"
RAW_CODEPO_GB_DIR = RAW_DIR / "codepo_gb"

if __name__ == "__main__":
    with open(
        EXTERNAL_CODEPO_GB_DIR / "Doc" / "Code-Point_Open_Column_Headers.csv",
        "r",
        encoding="ascii",
    ) as file_in:
        reader = csv.reader(file_in)
        next(reader)  # Skip abbreviated headers
        headers = [x.lower() for x in next(reader)]

    RAW_CODEPO_GB_DIR.mkdir()

    with open(
        RAW_CODEPO_GB_DIR / "codepo_gb.csv",
        "w",
        encoding="utf-8",
        newline="",
    ) as file_out:
        writer = csv.writer(file_out, dialect="unix")
        writer.writerow(headers)

        for path_in in (EXTERNAL_CODEPO_GB_DIR / "Data" / "CSV").iterdir():
            with path_in.open(encoding="ascii") as file_in:
                reader = csv.reader(file_in)
                writer.writerows(reader)
