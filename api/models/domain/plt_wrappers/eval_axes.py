from matplotlib.axes import Axes

class Eval_Axes(Axes):
    name = "eval_axes"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    ### Adding Data to the plot

    def plot(self, *args, **kwargs):
        return super().plot(*args, **kwargs)

    def errorbar(self, x, y, yerr=None, xerr=None, *args, **kwargs):
        return super().errorbar(x, y, yerr, xerr, *args, **kwargs)
        
    def scatter(self, x, y, *args, **kwargs):
        return super().scatter(x, y, *args, **kwargs)
        
    def fill_between(self, x, y1, y2=0, *args, **kwargs):
        return super().fill_between(x, y1, y2, *args, **kwargs)
        
    def bar(self, x, height, *args, **kwargs):
        return super().bar(x, height, *args, **kwargs)

    def stackplot(self, x, *args, **kwargs):
        return super().stackplot(x, *args, **kwargs)
        
    def boxplot(self, x, *args, **kwargs):
        return super().boxplot(x, *args, **kwargs)

    def hist(self, x, bins=None, *args, **kwargs):
        return super().hist(x, bins, *args, **kwargs)
