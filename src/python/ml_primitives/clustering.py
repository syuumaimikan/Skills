"""
Machine Learning and Data Science Primitives from Scratch:
- k-Means Clustering with k-means++ initialization
- k-Nearest Neighbors (k-NN) with Euclidean and Cosine Distance
- Fast Vector Normalization & Standardization
"""

import math
import random
from typing import List, Tuple, Dict, Optional, Literal, Any


def euclidean_distance(v1: List[float], v2: List[float]) -> float:
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(v1, v2)))


def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    dot = sum(a * b for a, b in zip(v1, v2))
    norm_a = math.sqrt(sum(a * a for a in v1))
    norm_b = math.sqrt(sum(b * b for b in v2))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


class KMeans:
    def __init__(self, k: int = 3, max_iter: int = 100, tol: float = 1e-4, seed: Optional[int] = 42):
        self.k = k
        self.max_iter = max_iter
        self.tol = tol
        self.seed = seed
        self.centroids: List[List[float]] = []

    def fit(self, data: List[List[float]]) -> "KMeans":
        if not data or len(data) < self.k:
            raise ValueError("Dataset size must be >= k")

        rng = random.Random(self.seed)
        dim = len(data[0])

        # k-means++ initialization
        self.centroids = [rng.choice(data)]
        for _ in range(1, self.k):
            distances = []
            for point in data:
                min_d = min(euclidean_distance(point, c) ** 2 for c in self.centroids)
                distances.append(min_d)
            total_d = sum(distances)
            if total_d == 0:
                self.centroids.append(rng.choice(data))
                continue
            probs = [d / total_d for d in distances]
            r = rng.random()
            cum = 0.0
            for point, p in zip(data, probs):
                cum += p
                if cum >= r:
                    self.centroids.append(point)
                    break

        for _ in range(self.max_iter):
            clusters: List[List[List[float]]] = [[] for _ in range(self.k)]
            for point in data:
                closest_idx = min(
                    range(self.k),
                    key=lambda idx: euclidean_distance(point, self.centroids[idx]),
                )
                clusters[closest_idx].append(point)

            new_centroids = []
            max_shift = 0.0
            for i, cluster in enumerate(clusters):
                if not cluster:
                    new_centroids.append(self.centroids[i])
                    continue
                new_c = [sum(p[d] for p in cluster) / len(cluster) for d in range(dim)]
                shift = euclidean_distance(new_c, self.centroids[i])
                max_shift = max(max_shift, shift)
                new_centroids.append(new_c)

            self.centroids = new_centroids
            if max_shift < self.tol:
                break

        return self

    def predict(self, points: List[List[float]]) -> List[int]:
        return [
            min(range(self.k), key=lambda idx: euclidean_distance(p, self.centroids[idx]))
            for p in points
        ]


class KNNClassifier:
    def __init__(self, k: int = 3, metric: Literal["euclidean", "cosine"] = "euclidean"):
        self.k = k
        self.metric = metric
        self.x_train: List[List[float]] = []
        self.y_train: List[Any] = []

    def fit(self, x: List[List[float]], y: List[Any]) -> "KNNClassifier":
        self.x_train = x
        self.y_train = y
        return self

    def predict_one(self, x: List[float]) -> Any:
        if self.metric == "euclidean":
            distances = [(euclidean_distance(x, train_x), label) for train_x, label in zip(self.x_train, self.y_train)]
            distances.sort(key=lambda t: t[0])
        else:
            distances = [(-cosine_similarity(x, train_x), label) for train_x, label in zip(self.x_train, self.y_train)]
            distances.sort(key=lambda t: t[0])

        top_k = [label for _, label in distances[: self.k]]
        # Majority voting
        vote_counts: Dict[Any, int] = {}
        for lbl in top_k:
            vote_counts[lbl] = vote_counts.get(lbl, 0) + 1
        return max(vote_counts.keys(), key=lambda k: vote_counts[k])

    def predict(self, x_list: List[List[float]]) -> List[Any]:
        return [self.predict_one(x) for x in x_list]
