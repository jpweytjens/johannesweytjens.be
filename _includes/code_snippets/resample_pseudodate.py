import itertools

import pandas as pd


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

    # combine alln products of household and dates in a single list
    result = [
        product
        for combination in combinations
        for product in itertools.product(*combination)
    ]
    mindex = pd.MultiIndex.from_tuples(result).set_names([group_id, pseudodate])

    # reindex as a faster alternative for .resample().asfreq()
    return df.set_index([group_id, pseudodate]).reindex(mindex).reset_index()
