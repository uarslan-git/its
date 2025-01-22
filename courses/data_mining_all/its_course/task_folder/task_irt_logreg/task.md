# Logistic Regression for IRT. 

Recall the one-parameter model from the Item Response Theory.

Write a function that uses logistic regression to fit a one-parameter IRT model to an input data matrix `X` and returns the vector of task difficulties. 

You can assume that the input matrix `X` has one row per student and one column per task. `X[i, j] = 1` if student $i$ got task $j$ right and `X[i, j] = 0`, otherwise.



