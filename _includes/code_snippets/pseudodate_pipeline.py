df = (
    df.pipe(add_pseudodate)
    .pipe(label_original_observations)
    .pipe(resample_missing_pseudodates)
    .pipe(fill_resampled_columns)
    .pipe(label_resampled_observations)
    .pipe(impute_resampled_dates)
    .pipe(remove_pseudodate)
)
