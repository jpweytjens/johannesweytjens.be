import matplotlib as mpl


def collect_artists(plot):
    """
    Collect relevant artists from a figure or axis.

    Parameters:
    plot : matplotlib.figure.Figure or matplotlib.axes.Axes
        The figure or axis object from which to collect artists.

    Returns:
    artists : list
        A list of collected artists.
    """
    artists = []
    if isinstance(plot, mpl.figure.Figure):
        for ax in plot.axes:
            artists.extend(_collect_artists(ax))

    if isinstance(plot, mpl.axes.Axes):
        artists.extend(_collect_artists(plot))

    return artists
