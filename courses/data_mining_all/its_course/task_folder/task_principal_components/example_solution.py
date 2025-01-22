#!function!#
import numpy as np
def principal_components(X, n):
#!prefix!#
    # compute the covariance matrix of the data
    cov     = np.cov(X.T)
    lambdas, V = np.linalg.eig(cov)

    # get the indices of the n largest eigenvalues
    idx = np.argsort(-lambdas)[:n]

    # extract V
    V = V[:, idx]

    # return
    return np.mean(X, 0), V
