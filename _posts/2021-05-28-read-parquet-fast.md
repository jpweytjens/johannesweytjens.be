---
layout: post
title: Read multiple (parquet) files with pandas fast
description: A function which uses python's built-in concurrent.futures package to read multiple (parquet) files with pandas in parallel.
permalink: read-multiple-files-with-pandas-fast/
date: 2021-08-04
---

Pandas is a great tool if your dataset fits in memory. Pandas however <a href="https://github.com/pandas-dev/pandas/issues/37955">does not provide a fast, parallel method to read most filetypes</a>. Instead, it relies on (external) engines to provide the parallelism. If your dataset does not fit in memory for example, there's a <a href="https://pandas.pydata.org/docs/ecosystem.html#ecosystem-out-of-core">list of libraries</a> such as <a href="https://docs.dask.org/en/latest/">dask</a> and <a href="https://github.com/modin-project/modin">modin</a> that do provide methods for both reading and working with large datasets in parallel with a pandas inspired API.

If you use plain pandas, you can still parallelize some common operations such as `apply` and `groupby` with <a href="https://github.com/nalepae/pandarallel">pandarallel</a>. What is still missing from this list, is a parallel method to read multiple files with pandas, regardless of the filetype. The code below provides such as function for parquet files, but the general idea can be applied to any <a href="https://pandas.pydata.org/docs/user_guide/io.html">filetype supported by pandas</a>.

The function below can read a large dataset, split across multiple files by reading the individual files in  parallel and concatenating them afterwards. The only requirements are `pandas` and a multicore processor. The code usses the built in Python modules `multiprocessing` and `concurrent.futures` modules and adds an optional <a href="https://github.com/tqdm/tqdm">tqdm</a> progress bar and some minor optimizations, inspired by some StackOverflow threads, to further increase speed.

{% highlight python %}
{% include code_snippets/read_parquet_fast.py %}
{% endhighlight %}
