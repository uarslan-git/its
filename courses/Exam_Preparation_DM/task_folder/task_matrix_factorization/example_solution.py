#!function!#
import numpy as np

def matrix_factorization_sgd(R, K, learning_rate=0.01, reg_param=0.01, epochs=100):

#!prefix!#
    """
    Perform matrix factorization using stochastic gradient descent (SGD).

    Parameters:
    - R (numpy array): User-item rating matrix.
    - K (int): Number of latent factors.
    - learning_rate (float): Learning rate for gradient descent.
    - reg_param (float): Regularization parameter.
    - epochs (int): Number of iterations.

    Returns:
    - User and item matrices (U, V).
    """

    num_users, num_items = R.shape

    # Initialize user and item matrices with random values
    U = np.random.rand(num_users, K)
    V = np.random.rand(num_items, K)

    for epoch in range(epochs):
        for i in range(num_users):
            for j in range(num_items):
                if R[i, j] > 0:  # If the rating is observed
                    eij = R[i, j] - np.dot(U[i, :], V[j, :].T)
                    U[i, :] += learning_rate * (eij * V[j, :] - reg_param * U[i, :])
                    V[j, :] += learning_rate * (eij * U[i, :] - reg_param * V[j, :])

        # Calculate the error (RMSE) at the end of each epoch (optional)
        error = np.sqrt(np.sum((R - np.dot(U, V.T))**2) / np.sum(R > 0))
        print(f"Epoch {epoch + 1}/{epochs}, RMSE: {error}")

    return U, V

# Example usage:
# Assuming R is the user-item rating matrix
# You may replace this with your actual data
#R = np.array([
#    [5, 0, 3, 0, 4],
#    [0, 2, 0, 4, 5],
#    [4, 0, 0, 0, 2],
#    [0, 3, 5, 0, 0],
#])

#K = 3  # Number of latent factors
#learning_rate = 0.01
#reg_param = 0.01
#epochs = 100

#U, V = matrix_factorization_sgd(R, K, learning_rate, reg_param, epochs)

# Get the reconstructed matrix
#R_reconstructed = np.dot(U, V.T)
#print("Reconstructed Matrix:")
#print(R_reconstructed)
