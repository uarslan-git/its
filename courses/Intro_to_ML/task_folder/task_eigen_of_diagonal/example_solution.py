#!function!#
import numpy as np 
#!prefix!#
def eigen_of_diagonal(matrix):
    # Extract the diagonal elements
    diagonal = np.diag(np.diag(matrix))
    
    # Compute eigenvalues and eigenvectors of the diagonal matrix
    eigenvalues, eigenvectors = np.linalg.eig(diagonal)
    
    return eigenvalues, eigenvectors


