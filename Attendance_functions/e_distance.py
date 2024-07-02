import numpy as np

@staticmethod
# / Compute the e-distance between two 128D features
def return_euclidean_distance(feature_1, feature_2):

    feature_1 = np.array(feature_1)

    feature_2 = np.array(feature_2)

    dist = np.sqrt(np.sum(np.square(feature_1 - feature_2)))
    return dist
