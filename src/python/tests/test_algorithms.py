import unittest
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


class TestAlgorithms(unittest.TestCase):
    def test_knapsack(self):
        weights = [2, 3, 4, 5]
        values = [3, 4, 5, 8]
        capacity = 5
        max_val, items = knapsack_01(weights, values, capacity)
        self.assertEqual(max_val, 8)
        self.assertEqual(items, [3])

    def test_lcs(self):
        s1 = "ABCBDAB"
        s2 = "BDCABA"
        length, lcs_str = longest_common_subsequence(s1, s2)
        self.assertEqual(length, 4)
        self.assertEqual(len(lcs_str), 4)

    def test_levenshtein(self):
        self.assertEqual(levenshtein_distance("kitten", "sitting"), 3)
        self.assertEqual(levenshtein_distance("rosettacode", "raisethysword"), 8)
        self.assertEqual(levenshtein_distance("findy", "findy"), 0)

    def test_matrix_chain(self):
        dims = [10, 20, 30, 40, 30]
        cost, paren = matrix_chain_multiplication(dims)
        self.assertGreater(cost, 0)
        self.assertIn("x", paren)

    def test_sorting_and_searching(self):
        arr = [9, -3, 5, 2, 6, 8, -6, 1, 3]
        sorted_arr = dual_pivot_quicksort(arr)
        self.assertEqual(sorted_arr, sorted(arr))

        self.assertEqual(binary_search(sorted_arr, 5), sorted_arr.index(5))
        self.assertEqual(binary_search(sorted_arr, 100), -1)

        self.assertEqual(exponential_search(sorted_arr, -3), sorted_arr.index(-3))
        self.assertEqual(exponential_search(sorted_arr, 999), -1)

    def test_ml_primitives(self):
        data = [[1.0, 1.0], [1.5, 2.0], [8.0, 8.0], [9.0, 8.5]]
        kmeans = KMeans(k=2, seed=42).fit(data)
        preds = kmeans.predict([[1.1, 1.2], [8.5, 8.2]])
        self.assertNotEqual(preds[0], preds[1])

        x_train = [[1.0, 1.0], [1.2, 1.1], [8.0, 8.0], [8.2, 8.1]]
        y_train = ["group_a", "group_a", "group_b", "group_b"]
        knn = KNNClassifier(k=3).fit(x_train, y_train)
        self.assertEqual(knn.predict_one([1.05, 1.05]), "group_a")
        self.assertEqual(knn.predict_one([8.1, 8.05]), "group_b")


if __name__ == "__main__":
    unittest.main()
