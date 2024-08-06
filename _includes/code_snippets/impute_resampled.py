import pandas as pd
from pandas.tseries.offsets import DateOffset
from tqdm.auto import tqdm


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
