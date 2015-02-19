import matplotlib.pyplot as _plt
import numpy as _np

__all__ = ["errorhist"]

def errorhist(data,
              bins=10,
              bin_range=None,
              yerr=None,
              normed=True,
              weights=None,
              color=None,
              hist_args={"histtype":"step"},
              err_args={},
              ax=None,
              ):
    """
    Plot a histogram with errorbars
    """

    data = _np.array(data)

    try:
        bins = int(bins)
    except:
        bin_range = [min(bins), max(bins)]
        bins = len(bins) - 1

    if bin_range is None and type(bins) is int:
        bin_range = [_np.min(data), _np.max(data)]

    if ax is None:
        ax = _plt.gca()

    if color is None:
        color = next(ax._get_lines.color_cycle)

    if normed is True:
        mask = _np.logical_and(data>=bin_range[0], data<=bin_range[1])
        num_events = _np.sum(mask)
        normalisation = bins/(num_events*(bin_range[1]-bin_range[0]))
    else:
        normalisation = 1

    histo, bin_edges = _np.histogram(data, bins, bin_range)

    bin_middles = 0.5*(bin_edges[1:] + bin_edges[:-1])
    if yerr is None:
        if weights is None:
            yerr = _np.sqrt(histo)
        else:
            yerr = _np.zeros(bins)
            for i, (a, b) in enumerate(zip(bin_edges[:-1], bin_edges[1:])):
                mask = _np.logical_and(data >= a, data < b)
                yerr[i] = _np.sqrt(_np.sum(weights[mask]**2))

    yerr *= normalisation

    ax.errorbar(
        bin_middles,
        histo*normalisation,
        fmt='none',
        ecolor=color,
        yerr=yerr,
        **err_args
    )
    hist, bin_edges, patches = ax.hist(
        data,
        bins,
        bin_range,
        color=color,
        normed=normed,
        **hist_args
    )

    _plt.draw_if_interactive()
    return hist, bin_edges, patches
