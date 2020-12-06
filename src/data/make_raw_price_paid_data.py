"""Reads external and writes raw Land Registry Price Paid Data CSVs.

The external CSV does not have a header row.
The raw CSV has a header row.
"""
import csv

from src import EXTERNAL_DIR, RAW_DIR

EXTERNAL_PP_DIR = EXTERNAL_DIR / "price_paid_data"
RAW_PP_DIR = RAW_DIR / "price_paid_data"

headers = [
    "id",
    "price",
    "date_of_transfer",
    "postcode",
    "property_type",
    "age",
    "duration",
    "paon",
    "saon",
    "street",
    "locality",
    "town_city",
    "district",
    "county",
    "ppd_category_type",
    "record_status",
]

if __name__ == "__main__":
    RAW_PP_DIR.mkdir()

    with open(
        EXTERNAL_PP_DIR / "pp-2019.csv",
        "r",
        encoding="iso-8859-1",
    ) as file_in, open(
        RAW_PP_DIR / "pp-2019.csv",
        "w",
        encoding="utf-8",
        newline="",
    ) as file_out:
        reader = csv.reader(file_in)
        writer = csv.writer(file_out, dialect="unix")
        writer.writerow(headers)
        writer.writerows(reader)
