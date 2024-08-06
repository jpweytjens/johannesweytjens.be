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
