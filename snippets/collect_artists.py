# --8<-- [start:_collect_artists]
import matplotlib as mpl
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
# --8<-- [end:_collect_artists]


# --8<-- [start:collect_artists]
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
# --8<-- [end:collect_artists]


if __name__ == "__main__":
    import tempfile

    mpl.use("Agg")
    fig, ax = plt.subplots()
    ax.plot([0, 1], [0, 1], label="line")
    ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1))
    ax.annotate("outside", xy=(1, 1), xytext=(1.3, 0.2), arrowprops={})
    filename = f"{tempfile.mkdtemp()}/figure.png"

    # --8<-- [start:save]
    fig.savefig(
        filename,
        bbox_extra_artists=collect_artists(fig),
        bbox_inches="tight",
    )
    # --8<-- [end:save]

    assert len(collect_artists(fig)) >= 2
