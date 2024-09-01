from typing import Any, Literal, Sequence
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

class PLT_Wrapper():
    """
    This class is meant to receive all calls to matplotlib.pyplot to be able to extract the plot's data, before passing it on to matplotlib.pyplot
    """
    
    def subplots(
        nrows: int = 1, ncols: int = 1, *args,
        sharex: bool | Literal["none", "all", "row", "col"] = False,
        sharey: bool | Literal["none", "all", "row", "col"] = False,
        squeeze: bool = True,
        width_ratios: Sequence[float] | None = None,
        height_ratios: Sequence[float] | None = None,
        subplot_kw: dict[str, Any] | None = None,
        gridspec_kw: dict[str, Any] | None = None,
        **fig_kw
    ) -> tuple[Figure, Any]:
        fig = plt.figure(**fig_kw)
        axs = fig.subplots(nrows=nrows, ncols=ncols, sharex=sharex, sharey=sharey,
                        squeeze=squeeze, subplot_kw=subplot_kw,
                        gridspec_kw=gridspec_kw, height_ratios=height_ratios,
                        width_ratios=width_ratios)
        return fig, axs
    
    def suptitle(self, t, **kwargs):
        return plt.suptitle(t, **kwargs)
    
    def plot(self, *args, **kwargs):
        return plt.plot(*args, **kwargs)
        
    def scatter(self, x, y, *args, **kwargs):
        return plt.scatter(x, y, *args, **kwargs)
        
    def bar(self, x, height, *args, **kwargs):
        return plt.bar(x, height, *args, **kwargs)
        
    def fill_between(self, x, y1, y2=0, *args, **kwargs):
        return plt.fill_between(x, y1, y2, *args, **kwargs)
        
    def hist(self, x, bins=None, *args, **kwargs):
        return plt.hist(x, bins, *args, **kwargs)
        
    def boxplot(self, x, *args, **kwargs):
        return plt.boxplot(x, *args, **kwargs)
    
    def errorbar(self, x, y, yerr=None, xerr=None, *args, **kwargs):
        return plt.errorbar(x, y, yerr, xerr, *args, **kwargs)