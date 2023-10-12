# Matrices
## Built in functions
You can use paragraphs.
Use Math expressions in math blocks with double-dollar-signs:
\$\$ Y = \frac{1}{n} \sum_{i=1}^{n}x_i \$\$
Inline Math is also possible \$ Y = \bar{X} \$
It is also possible to use code blocks like so:
```python
import numpy as np 
# Create arrays: Use build in functions
print(np.eye(3))
np.zeros((5,3))  # Note: Shape must be specified as a tuple!
```
```
[[1. 0. 0.]
 [0. 1. 0.]
 [0. 0. 1.]]

array([[0., 0., 0.],
       [0., 0., 0.],
       [0., 0., 0.],
       [0., 0., 0.],
       [0., 0., 0.]])
 ```
 ## To Do

Create a function that generates an identity matrix of a specified size, where all diagonal elements are set to a specific value other than 1.

```python
def custom_identity_matrix(n, value):
    ...
```
If the matrix cannot be created (negative n), return None. 