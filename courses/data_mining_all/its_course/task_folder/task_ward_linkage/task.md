# Ward linkage

To perform agglomerative clustering, one needs to define a distance between clusters.

Write a function that receives as input two clusters, given as data matrices `X` and `Y`, and returns the distance between both clusters according to Ward's method, which is the shared inter-cluster-variance, meaning the sum of squared distances to their shared mean:

$d(X, Y) = \frac{1}{|X| + |Y|} \cdot (\sum_{x \in X \cup Y} \lVert x - \mu\rVert^2)$

where $\mu$ is the shared mean of both clusters.
