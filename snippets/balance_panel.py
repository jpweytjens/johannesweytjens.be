# --8<-- [start:add_pseudodate]
import itertools

import pandas as pd
from pandas.tseries.offsets import DateOffset
from tqdm.auto import tqdm


def add_pseudodate(df, start_pseudodate=pd.Timestamp("1900-01-01")):
    # offset such that the first monthly date aligns
    # with the first daily date
    offset = df["date"].min().year * 12 + df["date"].min().month

    # map
    df["pseudodate"] = start_pseudodate + pd.to_timedelta(
        df["date"].dt.year * 12 + df["date"].dt.month - offset, unit="D"
    )

    return df
# --8<-- [end:add_pseudodate]


# --8<-- [start:resample_missing_pseudodates]
def resample_missing_pseudodates(
    df, pseudodate="pseudodate", group_id="group", method="fast"
):
    if method == "fast":
        return _resample_fast(df, pseudodate=pseudodate, group_id=group_id)

    if method == "slow":
        return _resample_slow(df, pseudodate=pseudodate, group_id=group_id)

    return df


def _resample_slow(df, pseudodate, group_id):
    return (
        df.set_index(pseudodate)
        .groupby(group_id)
        .resample("1D")
        .asfreq()
        .drop(columns=[group_id])
        .reset_index()
    )


def _resample_fast(df, pseudodate, group_id):
    # determine the first and last observation of each household
    date_ranges = df.groupby(group_id, as_index=False)[pseudodate].agg(["min", "max"])

    # construct all dates between the first and last date for each households
    combinations = [
        ([row[group_id]], list(pd.date_range(row["min"], row["max"], freq="D")))
        for _, row in date_ranges.iterrows()
    ]

    # combine all products of household and dates in a single list
    result = [
        product
        for combination in combinations
        for product in itertools.product(*combination)
    ]
    mindex = pd.MultiIndex.from_tuples(result).set_names([group_id, pseudodate])

    # reindex as a faster alternative for .resample().asfreq()
    return df.set_index([group_id, pseudodate]).reindex(mindex).reset_index()
# --8<-- [end:resample_missing_pseudodates]


# --8<-- [start:fill_resampled_columns]
def fill_resampled_columns(
    df,
    id_columns=["date", "resampled"],
    group_id="group",
    fill_value=0,
):
    id_columns = [group_id] + id_columns

    if isinstance(fill_value, (int, float)):
        columns = list(set(df.columns).difference(set(id_columns)))
        df[columns] = df[columns].fillna(fill_value)

    return df
# --8<-- [end:fill_resampled_columns]


# --8<-- [start:label_resampled]
def label_original_observations(df):
    df["resampled"] = False

    return df


def label_resampled_observations(df):
    df["resampled"] = df["resampled"].astype(bool).fillna(True)

    return df
# --8<-- [end:label_resampled]


# --8<-- [start:impute_resampled_dates]
def impute_resampled_dates(
    df,
    pseudodate="pseudodate",
    start_pseudodate=pd.Timestamp("1900-01-01"),
    progress_bar=True,
    group_id="group",
    imputed_date="date",
):
    df["offset_days"] = (df[pseudodate] - start_pseudodate).dt.days

    # adding a column of DateOffsets isn't vectorized
    # adding a single DateOffset IS vectorized
    # making this much faster than non vectorized approaches
    min_date = df["date"].min()
    for offset in tqdm(df["offset_days"].unique(), disable=not progress_bar):
        condition = df["offset_days"] == offset
        df.loc[condition, imputed_date] = min_date + DateOffset(months=offset)

    return df.drop(columns=["offset_days"]).sort_values(by=[group_id, "date"])
# --8<-- [end:impute_resampled_dates]


# --8<-- [start:remove_pseudodate]
def remove_pseudodate(df):
    return df.drop(columns=["pseudodate"])
# --8<-- [end:remove_pseudodate]


if __name__ == "__main__":
    df = pd.DataFrame(
        {
            "group": [1, 1, 2, 2],
            "date": pd.to_datetime(["2020-01-01", "2020-03-01", "2020-01-01", "2020-04-01"]),
            "income": [10.0, 30.0, 5.0, 20.0],
        }
    )

    # --8<-- [start:resample]
    balanced = (
        df.set_index("date")
        .groupby("group")
        .resample("MS")
        .asfreq()
        .reset_index()
    )
    # --8<-- [end:resample]

    import polars as pl

    # --8<-- [start:polars]
    upsampled = (
        pl.from_pandas(df)
        .sort("group", "date")
        .upsample("date", every="1mo", group_by="group")
        .to_pandas()
    )
    # --8<-- [end:polars]

    # --8<-- [start:pipeline]
    df = (
        df.pipe(add_pseudodate)
        .pipe(label_original_observations)
        .pipe(resample_missing_pseudodates)
        .pipe(fill_resampled_columns)
        .pipe(label_resampled_observations)
        .pipe(impute_resampled_dates)
        .pipe(remove_pseudodate)
    )
    # --8<-- [end:pipeline]

    assert len(df) == 7 and df["resampled"].sum() == 3
    grid = df[["group", "date"]].reset_index(drop=True)
    assert balanced[["group", "date"]].equals(grid)
    assert upsampled[["group", "date"]].astype(grid.dtypes).equals(grid)
