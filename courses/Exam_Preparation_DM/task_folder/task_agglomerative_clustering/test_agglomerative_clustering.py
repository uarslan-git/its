#this is not a test, but rather a visualization of how the data and other things can look like

from example_solution import agglomerative_clustering
import numpy as np
# Generate synthetic 2D data with three clusters
np.random.seed(42)

# First cluster around (2, 2)
cluster1 = np.random.normal(loc=[2, 2], scale=0.5, size=(20, 2))

# Second cluster around (6, 6)
cluster2 = np.random.normal(loc=[6, 6], scale=0.5, size=(20, 2))

# Third cluster around (10, 2)
cluster3 = np.random.normal(loc=[10, 2], scale=0.5, size=(20, 2))

# Concatenate the clusters to form the dataset
your_data = np.concatenate([cluster1, cluster2, cluster3])

# Visualize the data (optional)
import matplotlib.pyplot as plt

plt.scatter(your_data[:, 0], your_data[:, 1])
plt.title('Example 2D Data for Agglomerative Clustering')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.show()


# Example Usage
desired_number_of_clusters = 3
clusters = agglomerative_clustering(your_data, desired_number_of_clusters)

print("Cluster Labels:", clusters)