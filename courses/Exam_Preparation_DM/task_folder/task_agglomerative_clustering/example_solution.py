#!function!#
import numpy as np

def euclidean_distance(x, y):
    return np.linalg.norm(x - y)

def ward_linkage(cluster1, cluster2):
    n1, n2 = len(cluster1), len(cluster2)
    centroid1, centroid2 = np.mean(cluster1, axis=0), np.mean(cluster2, axis=0)
    return (n1 * n2 / (n1 + n2)) * euclidean_distance(centroid1, centroid2)**2

def find_closest_clusters(clusters, distances):
    min_distance = np.inf
    closest_clusters = (0, 0)

    for i in range(len(clusters)):
        for j in range(i + 1, len(clusters)):
            distance = distances[i, j]
            if distance < min_distance:
                min_distance = distance
                closest_clusters = (i, j)

    return closest_clusters


def agglomerative_clustering(data):
#!prefix!#
    # Initialize clusters
    clusters = [[point] for point in data]

    # Calculate pairwise Euclidean distances
    distances = np.zeros((len(clusters), len(clusters)))
    for i in range(len(clusters)):
        for j in range(i + 1, len(clusters)):
            distances[i, j] = euclidean_distance(np.mean(clusters[i], axis=0), np.mean(clusters[j], axis=0))
            distances[j, i] = distances[i, j]

    # Main loop for agglomerative clustering
    while len(clusters) > 1:
        i, j = find_closest_clusters(clusters, distances)
        clusters[i].extend(clusters[j])
        del clusters[j]

        # Update distances matrix
        for k in range(len(clusters)):
            if k != i:
                distances[i, k] = ward_linkage(clusters[i], clusters[k])
                distances[k, i] = distances[i, k]

    # Assign cluster labels
    labels = np.zeros(len(data), dtype=int)
    for i, cluster in enumerate(clusters):
        labels[cluster] = i

    return labels