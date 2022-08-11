from typing import List, Tuple
import numpy as np


def generate_data(
    means: List[Tuple[float]],
    n_points: List[int],
):
    """
    Generates clusterized data points.

    Args:
        means: List of the coordinates of the means of the generating gaussians. The length of the tuples should be consistent and determines the dimension.
        n_points: Number of point for each cluster. The length should be equal to the length of `means`.

    Returns:
        A 2D numpy array of shape (n_data_points, n_dim) containing the data points.
    """
    np.random.seed(1)
    means = np.array(means, dtype=np.float64)
    n_dim = means.shape[1]
    cov = np.eye(N=n_dim, dtype=np.float64)
    data_points = []
    for i, mean in enumerate(means):
        n_dim = mean.shape[0]
        data = np.random.multivariate_normal(mean, cov, size=n_points[i])
        data_points += list(data)
    data_points = np.array(data_points).squeeze()
    # Save data
    filename = "data_2D.txt"
    print(f"Saving data points in `{filename}`")
    np.savetxt(filename, data_points)
    # Return
    return data_points
