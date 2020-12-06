"""Reads external and writes raw Ordnance Survey Boundary-Line data.

External data is stored in a GeoPackage.
Raw data is stored in several GeoJSON files, one per layer.
"""
import geopandas
from src import EXTERNAL_DIR, RAW_DIR

EXTERNAL_BDLINE_DIR = EXTERNAL_DIR / "bdline_gpkg_gb"
RAW_BDLINE_DIR = RAW_DIR / "bdline_gb"  # It's no longer a GeoPackage

if __name__ == "__main__":
    RAW_BDLINE_DIR.mkdir()

    filename = EXTERNAL_BDLINE_DIR / "data" / "bdline_gb.gpkg"
    layers = ["district_borough_unitary"]
    for layer in layers:
        bdline_gb_layer = geopandas.read_file(filename, layer=layer)
        bdline_gb_layer.columns = bdline_gb_layer.columns.str.lower()

        # Land Registry Price Paid Data does not cover Scotland.
        rows = ~bdline_gb_layer.census_code.str.startswith("S")

        columns = ["census_code", "name", "geometry"]
        if not set(columns) < set(bdline_gb_layer.columns):
            print(f"Skipping {layer} because it is missing a required column")
            continue

        bdline_gb_layer.loc[rows, columns].to_file(
            RAW_BDLINE_DIR / f"{layer}.json", driver="GeoJSON"
        )
