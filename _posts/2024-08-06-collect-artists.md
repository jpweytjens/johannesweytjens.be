---
layout: post
title: Automatically include additional artists when using bbox_inches="tight"
description: Two functions that automatically take into account legends, labels and annotations when using bbox_inches="tight" whilst saving a matplotlib figure.
permalink: optimized-matplotlib-bbox-inches-tight/
date: 2024-08-06
---

When working with Matplotlib to create visualizations, saving figures with complex layouts can sometimes be challenging. This is especially true when your plots include <a href="https://matplotlib.org/stable/users/explain/axes/tight_layout_guide.html#legends-and-annotations">custom legends, annotations</a>, or axis labels that don’t fit well with the default saving behavior. The `bbox_inches="tight"` option can help by trimming excess white space, but it may not always account for all elements, leading to cropped legends or annotations. 

When you save a figure using Matplotlib, you might use the `bbox_inches="tight"` option to ensure that all elements are included without excessive whitespace. However, this option can sometimes fail to include custom legends, annotations, or other artists that lie outside the main axes area. This can result in a saved image where important elements are clipped or missing.

To address this, we can manually specify extra artists using the `bbox_extra_artists` parameter in the `savefig` function. However, manually collecting these artists for each plot can be tedious and error-prone. This is where our custom functions come into play.


The `_collect_artists` function is designed to collect the relevant artists from a given axis (`ax`). An artist in Matplotlib is a general term for any object that can be drawn on a figure (e.g., lines, text, patches).


{% highlight python %}
{% include code_snippets/_collect_artists.py %}
{% endhighlight %}

This function checks the axis (`ax`) for different types of artists such as legends, annotations, and axis titles/labels, and collects them into a list. This list is then returned, making it easy to manage the various elements in your plot.

The `collect_artists` function extends the `_collect_artists` function by applying it to either a whole figure or a single axis. This flexibility allows it to handle both simple and complex figures with multiple subplots.

{% highlight python %}
{% include code_snippets/collect_artists.py %}
{% endhighlight %}

This function first checks if the `plot` parameter is a figure or an axis. If it’s a figure, it iterates through all axes in the figure, collecting artists from each one. If it’s a single axis, it directly collects artists from that axis. The result is a list of all relevant artists, ready to be used when saving the figure.

To use these functions, you simply call `collect_artists` when saving your figure:

{% highlight python %}
{% include code_snippets/save_artists.py %}
{% endhighlight %}

This ensures that all the collected artists are included in the bounding box calculation, resulting in a well-cropped image without cutting off important elements.
