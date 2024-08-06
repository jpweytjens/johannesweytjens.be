def label_original_observations(df):
    df["resampled"] = False

    return df


def label_resampled_observations(df):
    df["resampled"] = df["resampled"].astype(bool).fillna(True)

    return df
