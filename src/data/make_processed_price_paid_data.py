"""Reads raw and writes processed Land Registry Price Paid Data.

Joins raw Land Registry Price Paid Data to processed Ordnance Survey
Code-Point Open data using the "shrunk" postcode (i.e. without white-space).
"""
import pandas

from src import PROCESSED_DIR, RAW_DIR
from src.data import helpers

RAW_PP_DIR = RAW_DIR / "price_paid_data"
PROCESSED_PP_DIR = PROCESSED_DIR / "price_paid_data"
PROCESSED_CODEPO_GB_DIR = PROCESSED_DIR / "codepo_gb"

POSTCODE_PATTERN = r"(?P<pc_area>\w{1,2})(?P<pc_district>\d{1,2}\w?)\s(?P<pc_sector>\d)(?P<pc_unit>\w{2})"  # NOQA

if __name__ == "__main__":
    dtype_string = {
        x: "string"
        for x in [
            "id",
            "postcode",
            "paon",
            "saon",
            "street",
            "locality",
            "town_city",
            "district",
            "county",
        ]
    }
    dtype_category = {
        x: "category"
        for x in [
            "property_type",
            "age",
            "duration",
            "ppd_category_type",
            "record_status",
        ]
    }
    pp_data = pandas.read_csv(
        RAW_PP_DIR / "pp-2019.csv",
        index_col="id",
        dtype={**dtype_string, **dtype_category},
        parse_dates=["date_of_transfer"],
        infer_datetime_format=True,
    )

    # We split each postcode into its area, district, sector, and unit parts.
    # It's faster to pass the string pattern rather than the compiled pattern.
    postcode_parts = pp_data.postcode.str.extract(POSTCODE_PATTERN)
    pp_data = pp_data.join(postcode_parts)

    # We join using the "shrunk" postcode, because the Land Registry and
    # the Ordnance Survey have different postcode formatting rules.
    pp_data["shrunk_postcode"] = pp_data.postcode.transform(helpers.shrink)
    codepo_gb = pandas.read_feather(
        PROCESSED_CODEPO_GB_DIR / "codepo_gb.feather",
    ).set_index("shrunk_postcode")
    pp_data = pp_data.join(
        codepo_gb,
        "shrunk_postcode",
        lsuffix="_pp_data",
        rsuffix="_codepo_gb",
    )

    PROCESSED_PP_DIR.mkdir()
    pp_data.reset_index().to_feather(PROCESSED_PP_DIR / "pp-2019.feather")
