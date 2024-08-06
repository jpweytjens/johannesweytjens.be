import matplotlib.pyplot as plt


def _collect_artists(ax):
    """
    Collect relevant artists from an axis.

    Parameters:
    ax : matplotlib.axes.Axes
        The axis object from which to collect artists.

    Returns:
    artists : list
        A list of collected artists.
    """
    artists = []

    # Collect legend
    if ax.get_legend() is not None:
        artists.append(ax.get_legend())

    # Collect annotations
    for artist in ax.get_children():
        if isinstance(artist, plt.Annotation):
            artists.append(artist)

    # Collect axis titles and labels
    if ax.title:
        artists.append(ax.title)
    if ax.xaxis.label:
        artists.append(ax.xaxis.label)
    if ax.yaxis.label:
        artists.append(ax.yaxis.label)

    return artists
