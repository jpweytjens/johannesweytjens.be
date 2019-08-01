---
layout: post
excerpt_separator: <!--more-->
title: Lorem ipsum
description: A test blog post
permalink: initial-post
date: 2019-07-29
---

## Header
This is some text

{% highlight python %}
import re
import pathlib
import natsort


def _filter_subdirectories(home, directories, min_level, max_level):
    """ Returns only pathlib directories within min_level and max_level subdirectories relative to home. """

    # normalize home path
    home = home.resolve()

    # define max and min directory depth in pathlib parts
    min_filter = len(home.parts) + min_level
    if max_level <= 0:
        max_filter = max(
            len(home.parts), max(map(lambda x: len(x.parts), directories)) + max_level
        )
    else:
        max_filter = len(home.parts) + max_level

    directories = list(
        filter(lambda x: min_filter <= len(x.parts) <= max_filter, directories)
    )

    return directories
{% endhighlight %}

