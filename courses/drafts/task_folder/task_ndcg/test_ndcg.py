from example_solution import ndcg_at_k
#!cut_imports!#
def test_ndcg():
    import numpy as np

    actual = [3, 2, 3, 0, 1, 2]  # Actual relevance scores
    predicted = [3, 2, 0, 0, 1, 4]  # Predicted relevance scores

    k_value = 5  # Position up to which to calculate nDCG

    #Test Output type
    res = ndcg_at_k(actual, predicted, k_value)    
    assert type(res) in [int, float, np.int_, np.float_], f"The return type of your function should be numeric but is {type(res)}"

    #Test normalized result
    for i in range(0,30):
        actual = np.random.randint(1, 3, 4)
        predicted = np.random.randint(1, 3, 4)
        res = ndcg_at_k(actual, predicted, 3) 
        assert (res <= 1 and res >= 0), f"nDCG shoul be normalized, meaning it should always be in [0, 1]"

    #Test exact result
    actual = [3, 2, 3, 0, 1, 2, 5, 2, 4]  # Actual relevance scores
    predicted = [3, 2, 0, 0, 1, 4, 3, 1, 4]  # Predicted relevance scores

    true_res = 0.8720625320870534
    res = ndcg_at_k(actual, predicted, 7)
    assert res == true_res, f"nDCG was not calculated correctly {res}" 

