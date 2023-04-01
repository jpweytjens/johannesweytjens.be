---
layout: post
title: Read multiple (parquet) files with pandas fast
description: A function which uses python's built-in concurrent.futures package to read multiple (parquet) files with pandas in parallel.
permalink: read-multiple-files-with-pandas-fast/
date: 2021-08-04
---

Pandas is an excellent choice for handling datasets that meet the following conditions:

   * The dataset is stored in a single file.
   * The dataset fits within the available memory.

If these conditions are not met, additional packages may be necessary for efficient data processing. For datasets that do not fit in memory, libraries such as  <a href="https://docs.dask.org/en/latest/">Dask</a> and <a href="https://github.com/modin-project/modin">Modin</a> provide out-of-memory processing and parallel loading capabilities, along with a pandas-inspired API.

These frameworks are well-suited for processing terabytes of data on large clusters but may be excessive for datasets that fit in memory but take a long time to load. Slow loading can occur when datasets are spread across multiple files that need to be concatenated. Moreover, these frameworks may not support the entire pandas API, depending on the specific analysis requirements.

To accelerate pandas operations with larger datasets that do not fully benefit from Dask or Modin, consider using <a href="https://github.com/nalepae/pandarallel">pandarallel</a> for parallelizing both apply and groupby.apply. Additionally,  <a href="https://github.com/zeehio/parmap">parmap</a>, a convenient wrapper around multiprocessing's Pool, provides a parallel map function for tasks that can be divided into independent parts.

However, a parallel method for reading multiple files with pandas, regardless of file type, is still needed. The following function demonstrates how to read a dataset split across multiple parquet.gz files by loading individual files in parallel and concatenating them afterward. This approach can be adapted for other <a href="https://pandas.pydata.org/docs/user_guide/io.html">filetype supported by pandas</a>.

The only requirements for this function are pandas, tqdm, and a multicore processor. The code utilizes Python's built-in concurrent.futures module, and incorporates an optional tqdm progress bar and minor optimizations inspired by StackOverflow discussions to further improve performance.

{% highlight python %}
{% include code_snippets/read_parquet_fast.py %}
{% endhighlight %}
