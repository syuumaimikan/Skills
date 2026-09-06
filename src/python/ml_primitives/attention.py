"""
Transformer Self-Attention & Multi-Head Attention Mechanism from Scratch (Pure Python)
"""

import math
import random
from typing import List, Tuple


def softmax(vector: List[float]) -> List[float]:
    max_val = max(vector)
    exp_vals = [math.exp(v - max_val) for v in vector]
    sum_exp = sum(exp_vals)
    return [v / sum_exp for v in exp_vals]


def matmul(a: List[List[float]], b: List[List[float]]) -> List[List[float]]:
    rows_a = len(a)
    cols_a = len(a[0])
    cols_b = len(b[0])

    result = [[0.0] * cols_b for _ in range(rows_a)]
    for i in range(rows_a):
        for k in range(cols_a):
            r = a[i][k]
            for j in range(cols_b):
                result[i][j] += r * b[k][j]
    return result


def transpose(matrix: List[List[float]]) -> List[List[float]]:
    return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]


class ScaledDotProductAttention:
    """
    Computes Attention(Q, K, V) = softmax(Q * K^T / sqrt(d_k)) * V
    """
    @staticmethod
    def forward(
        query: List[List[float]],
        key: List[List[float]],
        value: List[List[float]],
        mask: bool = False
    ) -> Tuple[List[List[float]], List[List[float]]]:
        seq_len = len(query)
        d_k = len(query[0])
        scale = math.sqrt(d_k)

        # 1. Q * K^T
        key_t = transpose(key)
        scores = matmul(query, key_t)

        # 2. Scale & Optional Causal Mask
        attention_weights = []
        for i in range(seq_len):
            row = [scores[i][j] / scale for j in range(len(scores[i]))]
            if mask:
                for j in range(i + 1, len(row)):
                    row[j] = -1e9  # Mask future tokens
            attention_weights.append(softmax(row))

        # 3. Attention Weights * V
        output = matmul(attention_weights, value)
        return output, attention_weights
