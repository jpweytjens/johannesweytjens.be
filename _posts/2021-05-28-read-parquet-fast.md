---
layout: post
title: Read many Parquet files into pandas in parallel
description: 'A dataset split over many files loads one file at a time. A short function reads them in parallel with Python''s standard library, for any format pandas reads.'
permalink: read-multiple-files-with-pandas-fast/
date: 2021-08-04
---

Pandas is an excellent choice for handling datasets that meet the following conditions:

   * The dataset is stored in a single file.
   * The dataset fits within the available memory.

If these conditions are not met, additional packages may be necessary for efficient data processing. For datasets that do not fit in memory, libraries such as <a href="https://docs.dask.org/en/latest/">Dask</a> and <a href="https://github.com/modin-project/modin">Modin</a> provide out-of-memory processing and parallel loading capabilities, along with a pandas-inspired API.

These frameworks are well-suited for processing terabytes of data on large clusters but may be excessive for datasets that fit in memory but take a long time to load. Slow loading can occur when datasets are spread across multiple files that need to be concatenated. Moreover, these frameworks may not support the entire pandas API, depending on the specific analysis requirements.

To accelerate pandas operations with larger datasets that do not fully benefit from Dask or Modin, consider using <a href="https://github.com/nalepae/pandarallel">pandarallel</a> for parallelizing both apply and groupby.apply. Additionally, <a href="https://github.com/zeehio/parmap">parmap</a>, a convenient wrapper around multiprocessing's Pool, provides a parallel map function for tasks that can be divided into independent parts.

However, a parallel method for reading multiple files with pandas, regardless of file type, is still needed. The following function demonstrates how to read a dataset split across multiple parquet.gz files by loading individual files in parallel and concatenating them afterward. This approach can be adapted for other <a href="https://pandas.pydata.org/docs/user_guide/io.html">file types supported by pandas</a>.

The only requirements for this function are pandas, tqdm, and a multicore processor. The code utilizes Python's built-in concurrent.futures module, and incorporates an optional tqdm progress bar and minor optimizations inspired by StackOverflow discussions to further improve performance.

{% snippet read_parquet.py read_parquet %}

The full script, with a small example that runs it, is [read_parquet.py]({{ site.baseurl }}/snippets/read_parquet.py).

## Addendum, October 2026

Given a directory, pandas reads every Parquet file in it and concatenates them in one call, at nearly the speed of the function above:

{% snippet read_parquet.py native %}

On a synthetic dataset of 64 gzip-compressed files, each 250,000 rows by 20 columns, the median of five reads took 2.69 s with `pd.read_parquet` and 2.54 s with `read_parquet`, on 12 cores with pandas 3.0.6 and pyarrow 25.0.1. Six percent rarely pays for a function to maintain, so the one-liner is the place to start. The function above still earns its keep when the files do not share a directory, or when a slow read needs a progress bar.
