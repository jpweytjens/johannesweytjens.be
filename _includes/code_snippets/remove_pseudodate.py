def remove_pseudodate(df):
    return df.drop(columns=["pseudodate"])
