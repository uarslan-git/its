from matplotlib.figure import Figure

class Eval_Figure(Figure):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_subplot(self, *args, **kwargs):
        # make sure the returned Axes are of the right projection
        if kwargs: kwargs['projection'] = "eval_axes"
        else: kwargs = {'projection': "eval_axes"}
        return super().add_subplot(*args, **kwargs)
    
    def savefig(self, *args, **kwargs):
        raise PermissionError("Method not allowed.")
        # return super().savefig(*args, **kwargs)
