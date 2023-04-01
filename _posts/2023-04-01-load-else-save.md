---
layout: post
title: Speed up slow computations that output pandas' DataFrames
description: A decorator to automatically save and load output from slow functions that return DataFrames.
permalink: load-else-save/
date: 2023-04-01
---

In data science, it's common to work with large datasets that require time-consuming and computationally expensive processing. During the development phase, you may frequently update a function that transforms and analyzes these datasets. However, regenerating the transformed dataset from scratch can be slow and inefficient. A caching decorator can help alleviate this issue by saving the computed dataset to disk and reloading it when needed, significantly reducing computation time.

The caching decorator `load_else_save` offers the following benefits:

* Computes the dataset once and saves it to disk.
* If the (slow) function is rerun, the dataset will be loaded from disk instead of being recomputed, saving time and computational resources.
* Automatically reruns the function and saves the new output if the source code changes, ensuring the output remains consistent with the updated function.

Adding full line comments or changing the formatting does not trigger the function to be rerun thanks to `black`. A small file with a hash of the source code is saved in a hidden directory `.decoration`. Removing this file, or copying the output without this directory, will trigger the function to be rerun.

By using a caching decorator, you can optimize the handling of large datasets and minimize the time spent waiting for results during the development phase. This approach enables you to focus on refining and improving your data analysis functions while avoiding unnecessary computations.

Here's an example of a caching decorator that saves the output as parquet files.

{% highlight python %}
{% include code_snippets/load_else_save.py %}
{% endhighlight %}
