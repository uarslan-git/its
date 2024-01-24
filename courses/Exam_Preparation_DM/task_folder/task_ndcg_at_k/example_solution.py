#!function!#
import numpy as np
def ndcg_at_k(actual, predicted, k):
#!prefix!#
    """
    Compute Normalized Discounted Cumulative Gain (nDCG) at a specified position k.

    Parameters:
    - actual (list): The list of actual relevance scores.
    - predicted (list): The list of predicted relevance scores.
    - k (int): The position up to which to calculate nDCG.

    Returns:
    - nDCG value.
    """
    def dcg_at_k(ranking):
        ranking = np.asarray(ranking)[:k]
        discounts = np.log2(np.arange(len(ranking)) + 2) # because it starts with 0 compared to the slides
        dcg = np.sum(ranking / discounts)
        return dcg

    ideal_sorted_order = np.argsort(actual)[::-1]
    ideal_dcg = dcg_at_k([actual[i] for i in ideal_sorted_order])

    predicted_sorted_order = np.argsort(predicted)[::-1]
    predicted_dcg = dcg_at_k([actual[i] for i in predicted_sorted_order])

    if ideal_dcg == 0:
        return 0  # Avoid division by zero

    ndcg = predicted_dcg / ideal_dcg
    return ndcg

# Example usage:
#actual_relevance = [3, 2, 3, 0, 1, 2]  # Actual relevance scores
#predicted_relevance = [3, 2, 0, 0, 1, 4]  # Predicted relevance scores

#k_value = 5  # Position up to which to calculate nDCG

#nDCG_value = ndcg_at_k(actual_relevance, predicted_relevance, k_value)
#print(f"nDCG at position {k_value}: {nDCG_value}")


