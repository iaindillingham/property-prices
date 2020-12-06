from pandas import Series


def shrink(series: Series) -> Series:
    return series.str.replace(r"\s+", "")
