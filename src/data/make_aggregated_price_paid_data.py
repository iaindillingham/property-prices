"""Aggregates processed Land Registry Price Paid Data.

Filters standard entries (category type A), groups by property type and
administrative district, and computes the median price.
"""
import numpy
import pandas

from src import PROCESSED_DIR

PROCESSED_PP_DIR = PROCESSED_DIR / "price_paid_data"
AGGREGATED_PP_DIR = PROCESSED_DIR / "aggregated_price_paid_data"

if __name__ == "__main__":
    pp_data = pandas.read_feather(PROCESSED_PP_DIR / "pp-2019.feather")
    pp_data = pp_data[pp_data.ppd_category_type == "A"]
    pp_data.property_type = pp_data.property_type.cat.rename_categories(
        {
            "D": "Detached",
            "F": "Flat",
            "O": "Other",
            "S": "Semi-Detached",
            "T": "Terraced",
        }
    )

    median_price = (
        pp_data.groupby(
            ["property_type", "admin_district_code"], observed=True
        )
        .aggregate({"price": numpy.median})
        .rename({"price": "median_price"})
    )

    AGGREGATED_PP_DIR.mkdir()
    median_price.to_csv(AGGREGATED_PP_DIR / "aggregated-pp-2019.csv")
