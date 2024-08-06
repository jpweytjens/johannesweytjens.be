import pandas as pd


def add_pseudodate(df, start_pseudodate=pd.Timestamp("1900-01-01")):
    # offset such that the first monthly date aligns
    # with the first daily date
    offset = df["date"].min().year * 12 + df["date"].min().month

    # map
    df["pseudodate"] = start_pseudodate + pd.to_timedelta(
        df["date"].dt.year * 12 + df["date"].dt.month - offset, unit="D"
    )

    return df
