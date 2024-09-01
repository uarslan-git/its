import matplotlib.pyplot as plt

class PLT_Wrapper():
    """
    This class is meant to receive all calls to matplotlib.pyplot to be able to extract the plot's data, before passing it on to matplotlib.pyplot
    """
    
    def subplots(self, nrows=1, ncols=1, *args, sharex=False, sharey=False, squeeze=True, width_ratios=None, height_ratios=None, subplot_kw=None, gridspec_kw=None, **fig_kw):
        return plt.subplots(nrows, ncols, *args, sharex, sharey, squeeze, width_ratios, height_ratios, subplot_kw, gridspec_kw, **fig_kw)
    
    def suptitle(self, t, **kwargs):
        return plt.suptitle(t, **kwargs)
    
    def plot(self, *args, scalex=True, scaley=True, data=None, **kwargs):
        return plt.plot(*args, scalex, scaley, data, **kwargs)
        
    def scatter(self, x, y, s=None, c=None, marker=None, cmap=None, norm=None, vmin=None, vmax=None, alpha=None, linewidths=None, *args, edgecolors=None, plotnonfinite=False, data=None, **kwargs):
        return plt.scatter(x, y, s, c, marker, cmap, norm, vmin, vmax, alpha, linewidths, *args, edgecolors, plotnonfinite, data, **kwargs)
        
    def bar(self, x, height, width=0.8, bottom=None, *args, align='center', data=None, **kwargs):
        return plt.bar(x, height, width, bottom, *args, align, data, **kwargs)
        
    def fill_between(self, x, y1, y2=0, where=None, interpolate=False, step=None, *args, data=None, **kwargs):
        return plt.fill_between(x, y1, y2, where, interpolate, step, *args, data, **kwargs)
        
    def hist(self, x, bins=None, range=None, density=False, weights=None, cumulative=False, bottom=None, histtype='bar', align='mid', orientation='vertical', rwidth=None, log=False, color=None, label=None, stacked=False, *args, data=None, **kwargs):
        return plt.hist(x, bins, range, density, weights, cumulative, bottom, histtype, align, orientation, rwidth, log, color, label, stacked, *args, data, **kwargs)
        
    def boxplot(self, x, notch=None, sym=None, vert=None, whis=None, positions=None, widths=None, patch_artist=None, bootstrap=None, usermedians=None, conf_intervals=None, meanline=None, showmeans=None, showcaps=None, showbox=None, showfliers=None, boxprops=None, tick_labels=None, flierprops=None, medianprops=None, meanprops=None, capprops=None, whiskerprops=None, manage_ticks=True, autorange=False, zorder=None, capwidths=None, label=None, *args, data=None):
        return plt.boxplot(x, notch, sym, vert, whis, positions, widths, patch_artist, bootstrap, usermedians, conf_intervals, meanline, showmeans, showcaps, showbox, showfliers, boxprops, tick_labels, flierprops, medianprops, meanprops, capprops, whiskerprops, manage_ticks, autorange, zorder, capwidths, label, *args, data)
    
    def errorbar(self, x, y, yerr=None, xerr=None, fmt='', ecolor=None, elinewidth=None, capsize=None, barsabove=False, lolims=False, uplims=False, xlolims=False, xuplims=False, errorevery=1, capthick=None, *args, data=None, **kwargs):
        return plt.errorbar(x, y, yerr, xerr, fmt, ecolor, elinewidth, capsize, barsabove, lolims, uplims, xlolims, xuplims, errorevery, capthick, *args, data, **kwargs)