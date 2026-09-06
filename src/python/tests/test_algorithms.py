import pytest
from src.python.algorithms.dynamic_programming import (
    knapsack_01,
    longest_common_subsequence,
    levenshtein_distance,
    matrix_chain_multiplication,
)
from src.python.algorithms.sorting_searching import (
    dual_pivot_quicksort,
    binary_search,
    exponential_search,
)
from src.python.ml_primitives.clustering import (
    KMeans,
    KNNClassifier,
    euclidean_distance,
    cosine_similarity,
)


def test_knapsack():
    weights = [2, 3, 4, 5]
    values = [3, 4, 5, 8]
    capacity = 5
    max_val, items = knapsack_01(weights, values, capacity)
    assert max_val == 8
    assert items == [3]  # item with weight 5 and val 8


def test_lcs():
    s1 = "ABCBDAB"
    s2 = "BDCABA"
    length, lcs_str = longest_common_subsequence(s1, s2)
    assert length == 4
    assert len(lcs_str) == 4


def test_levenshtein():
    assert levenshtein_distance("kitten", "sitting") == 3
    assert levenshtein_distance("rosettacode", "raisethysword") == 8
    assert levenshtein_distance("findy", "findy") == 0


def test_matrix_chain():
    dims = [10, 20, 30, 40, 30]
    cost, paren = matrix_chain_multiplication(dims)
    assert cost > 0
    assert "x" in paren


def test_sorting_and_searching():
    arr = [9, -3, 5, 2, 6, 8, -6, 1, 3]
    sorted_arr = dual_pivot_quicksort(arr)
    assert sorted_arr == sorted(arr)

    assert binary_search(sorted_arr, 5) == sorted_arr.index(5)
    assert binary_search(sorted_arr, 100) == -1

    assert exponential_search(sorted_arr, -3) == sorted_arr.index(-3)
    assert exponential_search(sorted_arr, 999) == -1


def test_ml_primitives():
    # Test k-Means
    data = [[1.0, 1.0], [1.5, 2.0], [8.0, 8.0], [9.0, 8.5]]
    kmeans = KMeans(k=2, seed=42).fit(data)
    preds = kmeans.predict([[1.1, 1.2], [8.5, 8.2]])
    assert preds[0] != preds[1]  # belongs to different clusters

    # Test k-NN
    x_train = [[1.0, 1.0], [1.2, 1.1], [8.0, 8.0], [8.2, 8.1]]
    y_train = ["group_a", "group_a", "group_b", "group_b"]
    knn = KNNClassifier(k=3).fit(x_train, y_train)
    assert knn.predict_one([1.05, 1.05]) == "group_a"
    assert knn.predict_one([8.1, 8.05]) == "group_b"
