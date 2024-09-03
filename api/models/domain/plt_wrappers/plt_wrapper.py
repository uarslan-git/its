import matplotlib.pyplot as _plt
from api.models.domain.plt_wrappers.eval_figure import Eval_Figure
from api.models.domain.plt_wrappers.eval_axes import Eval_Axes
from matplotlib.projections import register_projection

"""
This wrapper is supposed to extract data plotted by students and process them.
WARNING: Students can still access the plt import in this module,
    so this is not 100% secure, since imports cannot be made private (thanks python).
Methods student are not supposed to have access to are simply ommitted from here.
"""

# TODO process data before forwarding to plt

### Managing Figure and Axes

def figure(**fig_kw):
    fig_kw = set_figure_class_arg(fig_kw)
    return _plt.figure(**fig_kw)

def subplots(*args, **fig_kw):
    fig_kw = set_figure_class_arg(fig_kw)
    return _plt.subplots(*args, **fig_kw)

def subplot(*args, **kwargs):
    return _plt.subplot(*args, **kwargs)

### Adding Data to the plot

def plot(*args, **kwargs):
    return _plt.plot(*args, **kwargs)

def errorbar(x, y, yerr=None, xerr=None, *args, **kwargs):
    return _plt.errorbar(x, y, yerr, xerr, *args, **kwargs)
    
def scatter(x, y, *args, **kwargs):
    return _plt.scatter(x, y, *args, **kwargs)
    
def fill_between(x, y1, y2=0, *args, **kwargs):
    return _plt.fill_between(x, y1, y2, *args, **kwargs)
    
def bar(x, height, *args, **kwargs):
    return _plt.bar(x, height, *args, **kwargs)

def stackplot(x, *args, **kwargs):
    return _plt.stackplot(x, *args, **kwargs)
    
def boxplot(x, *args, **kwargs):
    return _plt.boxplot(x, *args, **kwargs)

def hist(x, bins=None, *args, **kwargs):
    return _plt.hist(x, bins, *args, **kwargs)

### Axis configuration

def xlabel(label, *args, **kwargs):
    return _plt.xlabel(label, *args, **kwargs)

def xlim(*args, **kwargs):
    return _plt.xlim(*args, *kwargs)

def xscale(value, **kwargs):
    return _plt.xscale(value, *kwargs)

def xticks(ticks=None, labels=None, *args, **kwargs):
    return _plt.xticks(ticks, labels, *args, *kwargs)

def ylabel(label, *args, **kwargs):
    return _plt.ylabel(label, *args, *kwargs)

def ylim(*args, **kwargs):
    return _plt.ylim(*args, *kwargs)

def yscale(value, **kwargs):
    return _plt.yscale(value, *kwargs)

def yticks(ticks=None, labels=None, *args, **kwargs):
    return _plt.yticks(ticks, labels, *args, *kwargs)

def suptitle(t, **kwargs):
    return _plt.suptitle(t, **kwargs)

def title(label, *args, **kwargs):
    return _plt.title(label, *args, **kwargs)

### Output

def draw():
    return _plt.draw()

def show(*args, **kwargs):
    print("SHOWING")
    return _plt.show(*args, **kwargs)

### Utility

def set_figure_class_arg(kwargs):
    if kwargs: kwargs['FigureClass'] = Eval_Figure
    else: kwargs = {'FigureClass': Eval_Figure}
    return kwargs

def setup():
    register_projection(Eval_Axes)
    _plt.close('all')
    figure()
setup()
