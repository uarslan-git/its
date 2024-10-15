import example_solution
from .models.plt_wrappers.plt_wrapper import PLT_Wrapper
#!cut_imports!#
def test_graph_test():
    # TODO
    example_solution.plt = PLT_Wrapper()
    X = [[1, 2], [3, 4]]
    assert example_solution.plot_points(X)