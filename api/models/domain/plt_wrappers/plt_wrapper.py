import matplotlib.pyplot as plt
from api.models.domain.plt_wrappers.eval_figure import Eval_Figure
from api.models.domain.plt_wrappers.eval_axes import Eval_Axes
from matplotlib.projections import register_projection

### Managing Figure and Axes

def figure(**fig_kw):
    fig_kw = set_figure_class_arg(fig_kw)
    return plt.figure(**fig_kw)

def subplots(*args, **fig_kw):
    fig_kw = set_figure_class_arg(fig_kw)
    return plt.subplots(*args, **fig_kw)

def subplot(*args, **kwargs):
    return plt.subplot(*args, **kwargs)

### Adding Data to the plot

def plot(*args, **kwargs):
    return plt.plot(*args, **kwargs)

def errorbar(x, y, yerr=None, xerr=None, *args, **kwargs):
    return plt.errorbar(x, y, yerr, xerr, *args, **kwargs)
    
def scatter(x, y, *args, **kwargs):
    return plt.scatter(x, y, *args, **kwargs)
    
def fill_between(x, y1, y2=0, *args, **kwargs):
    return plt.fill_between(x, y1, y2, *args, **kwargs)
    
def bar(x, height, *args, **kwargs):
    return plt.bar(x, height, *args, **kwargs)

def stackplot(x, *args, **kwargs):
    return plt.stackplot(x, *args, **kwargs)
    
def boxplot(x, *args, **kwargs):
    return plt.boxplot(x, *args, **kwargs)

def hist(x, bins=None, *args, **kwargs):
    return plt.hist(x, bins, *args, **kwargs)

### Axis configuration

def xlabel(label, *args, **kwargs):
    return plt.xlabel(label, *args, **kwargs)

def xlim(*args, **kwargs):
    return plt.xlim(*args, *kwargs)

def xscale(value, **kwargs):
    return plt.xscale(value, *kwargs)

def xticks(ticks=None, labels=None, *args, **kwargs):
    return plt.xticks(ticks, labels, *args, *kwargs)

def ylabel(label, *args, **kwargs):
    return plt.ylabel(label, *args, *kwargs)

def ylim(*args, **kwargs):
    return plt.ylim(*args, *kwargs)

def yscale(value, **kwargs):
    return plt.yscale(value, *kwargs)

def yticks(ticks=None, labels=None, *args, **kwargs):
    return plt.yticks(ticks, labels, *args, *kwargs)

def suptitle(t, **kwargs):
    return plt.suptitle(t, **kwargs)

def title(label, *args, **kwargs):
    return plt.title(label, *args, **kwargs)

### Output

def draw():
    return plt.draw()

def show(*args, **kwargs):
    print("SHOWING")
    return plt.show(*args, **kwargs)

### Utility

def set_figure_class_arg(kwargs):
    if kwargs: kwargs['FigureClass'] = Eval_Figure
    else: kwargs = {'FigureClass': Eval_Figure}
    return kwargs

def setup():
    register_projection(Eval_Axes)
    plt.close('all')
    figure()
setup()
