from example_solution import matrix_factorization_sgd
#!cut_imports!#
def test_matrix_factorization():
    import numpy as np

    R = np.array([
        [5, 0, 3, 0, 4],
        [0, 2, 0, 4, 5],
        [4, 0, 0, 0, 2],
        [0, 3, 5, 0, 0],])

    #Test output type
    res = matrix_factorization_sgd(R, 3)
    assert type(res)==tuple, f"You should return the tuple $$(U, V)$$ with $$UV^t = R$$, you returned {type(res)}"
    assert len(res[0].shape)==2, f"$$U$$ should be a matrix like numpy array with two dimensions"
    assert len(res[1].shape)==2, f"$$V$$ should be a matrix like numpy array with two dimensions"

    #Non-positive K's should not be accepted.
    failed = True
    try:
        res = matrix_factorization_sgd(R, 0)
    except Exception:
        failed = False
    assert not failed, "You should not accept non-positive input values of K"

    #Test exact result.
    for i in range(0, 10):
        R = np.random.randint(-3, 3, (3,2))
        K = i+5
        U, V = matrix_factorization_sgd(R, K, learning_rate=0.1, epochs=1000)
        recon_R = (np.dot(U, V.T) - R)
        assert (np.abs(recon_R-R) < 0.1).all(), f"Matrix {str(R)} could not be reconstructed with K=={K}, result was {recon_R}"
