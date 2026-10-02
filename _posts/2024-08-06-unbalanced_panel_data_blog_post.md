---
layout: post
title: Fill gaps in an unbalanced panel before taking diffs or lags
description: 'pandas treats consecutive rows as consecutive periods, so `.diff()` and `.shift()` go wrong when a unit skips one. A fast way to insert the missing periods, including uneven ones such as months.'
permalink: resample-unbalanced-dataset-in-pandas-fast/
date: 2024-08-06
---


Working with panel data can be challenging, particularly when the data is unbalanced, meaning the observations do not occur at regular intervals. This irregularity poses a problem when applying operations like `.diff()` or `.shift()`, as Pandas assumes consecutive observations correspond to consecutive time periods. Without a fixed periodicity, calculating differences or shifts correctly becomes difficult. To address this, we can use a series of custom functions to balance the dataset by generating the missing intermediate values for every column if required. These new resampled values by default are set to NaN.

In this blog post, we’ll explore a set of custom functions designed to handle unbalanced panel data in Pandas. These functions will allow you to add a pseudodate, resample missing dates, fill missing values, and ensure that your data is correctly aligned for time-based operations.

The `add_pseudodate` function adds a pseudodate column to the dataframe, aligning irregular time periods to a continuous timeline. This is crucial for operations that require a consistent time index.

{% snippet balance_panel.py add_pseudodate %}

This function calculates an offset based on the minimum date in your dataset and maps each date to a corresponding pseudodate, starting from a specified `start_pseudodate`. The result is a new column in your dataframe that maintains temporal continuity.

Once the pseudodate is added, we need to fill in the missing dates. The `resample_missing_pseudodates` function offers two methods (`fast` and `slow`) to resample the data. The `slow` method is the straightforward pandas approach. This can be slow for panel datasets with high N (~500'000) and comparatively small T (~100). The `fast` method manually constructs a new `MultiIndex` with all the required observations and is about 4 times faster than the slow method.

{% snippet balance_panel.py resample_missing_pseudodates %}


Once missing dates are resampled, the next step is to fill in the missing values in the resampled columns.

{% snippet balance_panel.py fill_resampled_columns %}

This function fills the missing values with a specified `fill_value`, ensuring that your dataset is complete and ready for further analysis. These two functions add labels to a new column `resampled` to differentiate between original and resampled data points.

{% snippet balance_panel.py label_resampled %}

The `impute_resampled_dates` function adjusts the pseudodates back to actual dates, maintaining the temporal alignment. Currently, pandas (v2.2.2) doesn't support vectorized additions of DateOffsets, i.e. adding a column of DateOffsets to a datetime column. Pandas does allow fast addition of a single DateOffset to a datetime column. The function below partially vectorizes the addition by looping over all unique DateOffset values. If T is small compared to N, this is much faster than other approaches.

{% snippet balance_panel.py impute_resampled_dates %}

This function ensures that the imputed dates align with the original date values, keeping the data consistent.

Finally, the `remove_pseudodate` function cleans up the dataframe by removing the pseudodate column, leaving you with a balanced dataset ready for analysis.

{% snippet balance_panel.py remove_pseudodate %}

To use these functions, you can chain them together using Pandas’ `pipe` function:

{% snippet balance_panel.py pipeline %}

This pipeline will take your unbalanced panel data, fill in the missing values, and prepare it for time series operations like `.diff()` or `.shift()`.

The full script, with a small example that runs it, is [balance_panel.py]({{ site.baseurl }}/snippets/balance_panel.py).

## Addendum, October 2026

pandas fills the gaps itself when each unit is resampled at the start of every month, with no pseudodates:

{% snippet balance_panel.py resample %}

It is the place to start, and for a small panel the only code needed. On a large panel it is slow. On a synthetic panel of 20,000 units over 100 months with 30% of the months missing, the median of five runs took 8.2 s against 3.4 s for the pipeline above, on 12 cores with pandas 3.0.6. Polars has the operation built in, calendar months included, and took 2.3 s:

{% snippet balance_panel.py polars %}

All three return the same rows. Polars and `resample` leave the new rows empty; the pipeline above also fills and labels them.
