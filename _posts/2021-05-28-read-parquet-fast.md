---
layout: post
title: Read multiple (parquet) files with pandas fast
description: A function which uses python's built-in concurrent.futures package to read multiple (parquet) files with pandas in parallel.
permalink: read-multiple-files-with-pandas-fast/
date: 2021-08-04
---

Pandas is a great tool if your dataset consists of a single file that fits in memory. If both of these are not the case, you need to rely on <a href="https://github.com/pandas-dev/pandas/issues/37955">external packages.</a>. If your dataset does not fit in memory for example, there's a <a href="https://pandas.pydata.org/docs/ecosystem.html#ecosystem-out-of-core">list of libraries</a> such as <a href="https://docs.dask.org/en/latest/">dask</a> and <a href="https://github.com/modin-project/modin">modin</a> that provide methods for both out-of-memory processing and parallel loading of large datasets with a pandas inspired API. 

These frameworks are great when analyzing TB's of data one large clusters, but are overkill when your dataset is small enough to fit in memory, but is just slow to load. Loading data can be slow when e.g. your dataset is spread across multiple files that need to concatenated. Depending on your exact needs for your analysis, these frameworks <a href="https://modin.readthedocs.io/en/latest/supported_apis/index.html">do not currently support the entire pandas API</a> . 

So, what is the best way to speed up pandas with larger datasets that are too small to fully benefit from frameworks such as Dask or Modin? Once the data is loaded into memory, you can parallelize some common operations such as `apply` and `groupby` with <a href="https://github.com/nalepae/pandarallel">pandarallel</a>. Other tasks that can be easily split in independent parts, can be parallelized with <a href="https://github.com/zeehio/parmap">parmap</a>, a convenient wrapper using `multiprocessing`'s `Pool` to provide a parallel `map` function. What is still missing is a parallel method to read multiple files with pandas, regardless of the filetype. The code below provides such as function for parquet files, but the general idea can be applied to any <a href="https://pandas.pydata.org/docs/user_guide/io.html">filetype supported by pandas</a>.

The function below can read a dataset, split across multiple files by reading the individual files in  parallel and concatenating them afterwards. The only requirements are `pandas`, `tqdm` and a multicore processor. The code uses the built in Python module `concurrent.futures` modules and adds an optional <a href="https://github.com/tqdm/tqdm">`tqdm`</a> progress bar and some minor optimizations, inspired by some StackOverflow threads, to further increase speed.

{% highlight python %}
{% include code_snippets/read_parquet_fast.py %}
{% endhighlight %}
