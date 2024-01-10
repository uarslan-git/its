from example_solution import pooled_variance
#!cut_imports!#
def test_pooled_variance():

    sample1 = [2,1,2,1,2,1,2]
    n1 = len(sample1)
    x_var = sum((x - sum(sample1) / n1) ** 2 for x in sample1) / (n1 - 1) if n1 > 1 else 0.0

    #Test the correct output type
    res = pooled_variance(sample1,sample1)
    assert type(res) in [float, int], f"Output type should be numeric, is {type(res)}"

    #Pooled variance of equal sequences
    res = pooled_variance(sample1,sample1)
    assert  res == 2*x_var/n1, f"The pooled variance of a sequence with itsself should be equal to 2*variance/n"

    n1 = [1,2,2,4,7,6,8]
    n2 = [8,3,3,6,3]

    res = pooled_variance(n1, n2)
    true_res = 2.1416326530612246
    assert res == true_res, f"Wrong result for pooled variance"
