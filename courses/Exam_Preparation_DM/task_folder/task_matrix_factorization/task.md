# Stochastic Gradient Descent (SGD) for Matrix Factorization

Factorization of the rating matrix is a common techniques for the recommender systems. There are many variation both to the methods and to the optimization of the algorthm. 
In the homework, you could get to know the singular value descomposition (SVD) method. 

Here, we would like to introduce another method: stochastic gradient descent. 


## Algorithm

1. **Initialize Matrices**: Randomly initialize the user matrix $ U $ and item matrix $ V $.

2. **Stochastic Gradient Descent Iteration**:
   - For each observed rating $ R_{ij} $:
     - Compute the error $ e_{ij} = R_{ij} - U_i \cdot V_j^T $.
     - Update user and item matrices:
       - $ U_i \leftarrow U_i + \text{{learning_rate}} \cdot (e_{ij} \cdot V_j - \text{{reg_param}} \cdot U_i) $.
       - $ V_j \leftarrow V_j + \text{{learning_rate}} \cdot (e_{ij} \cdot U_i - \text{{reg_param}} \cdot V_j) $.

3. **Repeat**: Perform the stochastic gradient descent updates for a specified number of epochs.

4. **Output**: The final user matrix $ U $ and item matrix $ V $ represent the decomposed matrices capturing latent factors.

## Formulas

- **Error Term $ e_{ij} $**:
  $ e_{ij} = R_{ij} - U_i \cdot V_j^T $

- **User Matrix Update**:
  $ U_i \leftarrow U_i + \text{{learning_rate}} \cdot (e_{ij} \cdot V_j - \text{{reg_param}} \cdot U_i) $

- **Item Matrix Update**:
  $ V_j \leftarrow V_j + \text{{learning_rate}} \cdot (e_{ij} \cdot U_i - \text{{reg_param}} \cdot V_j) $

## Parameters

- **R**: User-item rating matrix.
- **U, V**: User and item matrices.
- **learning_rate**: Learning rate for gradient descent updates.
- **reg_param**: Regularization parameter to prevent overfitting.
- **epochs**: Number of iterations.

## Task

Please write a function for the matrix factorization, which will be using the SGD to approximate user and item matrices.