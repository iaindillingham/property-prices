"""Reads raw and writes processed Ordnance Survey Code-Point Open data.
"""
import pandas

from src import PROCESSED_DIR, RAW_DIR
from src.data import helpers

RAW_CODEPO_GB_DIR = RAW_DIR / "codepo_gb"
PROCESSED_CODEPO_GB_DIR = PROCESSED_DIR / "codepo_gb"


if __name__ == "__main__":
    dtype_string = {x: "string" for x in ["postcode", "admin_ward_code"]}
    dtype_category = {
        x: "category"
        for x in [
            "country_code",
            "nhs_regional_ha_code",
            "nhs_ha_code",
            "admin_county_code",
            "admin_district_code",
        ]
    }
    codepo_gb = pandas.read_csv(
        RAW_CODEPO_GB_DIR / "codepo_gb.csv",
        dtype={**dtype_string, **dtype_category},
    )
    codepo_gb["shrunk_postcode"] = codepo_gb.postcode.transform(helpers.shrink)

    PROCESSED_CODEPO_GB_DIR.mkdir()
    codepo_gb.to_feather(PROCESSED_CODEPO_GB_DIR / "codepo_gb.feather")
