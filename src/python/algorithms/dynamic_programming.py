"""
Advanced Dynamic Programming Algorithms:
- 0/1 Knapsack Problem (with item reconstruction)
- Longest Common Subsequence (LCS)
- Matrix Chain Multiplication (Optimal Parenthesization)
- Levenshtein Edit Distance with Operation Alignment
"""

from typing import List, Tuple, Dict, Any


def knapsack_01(weights: List[int], values: List[int], capacity: int) -> Tuple[int, List[int]]:
    """
    Solves 0/1 Knapsack problem with dynamic programming.
    Returns (maximum_value, list_of_selected_item_indices).
    """
    n = len(weights)
    if n == 0 or capacity <= 0:
        return 0, []

    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        w = weights[i - 1]
        v = values[i - 1]
        for c in range(capacity + 1):
            if w <= c:
                dp[i][c] = max(dp[i - 1][c], dp[i - 1][c - w] + v)
            else:
                dp[i][c] = dp[i - 1][c]

    # Reconstruct chosen items
    selected_indices = []
    curr_c = capacity
    for i in range(n, 0, -1):
        if dp[i][curr_c] != dp[i - 1][curr_c]:
            selected_indices.append(i - 1)
            curr_c -= weights[i - 1]

    selected_indices.reverse()
    return dp[n][capacity], selected_indices


def longest_common_subsequence(s1: str, s2: str) -> Tuple[int, str]:
    """
    Computes the Longest Common Subsequence between s1 and s2.
    Returns (lcs_length, lcs_string).
    """
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    # Reconstruct LCS string
    lcs_chars = []
    i, j = m, n
    while i > 0 and j > 0:
        if s1[i - 1] == s2[j - 1]:
            lcs_chars.append(s1[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1

    lcs_chars.reverse()
    return dp[m][n], "".join(lcs_chars)


def levenshtein_distance(s1: str, s2: str) -> int:
    """
    Computes minimum Levenshtein edit distance between s1 and s2.
    Space-optimized O(min(m, n)) solution.
    """
    if len(s1) < len(s2):
        s1, s2 = s2, s1

    prev_row = list(range(len(s2) + 1))

    for i, c1 in enumerate(s1):
        curr_row = [i + 1] * (len(s2) + 1)
        for j, c2 in enumerate(s2):
            insertions = prev_row[j + 1] + 1
            deletions = curr_row[j] + 1
            substitutions = prev_row[j] + (c1 != c2)
            curr_row[j + 1] = min(insertions, deletions, substitutions)
        prev_row = curr_row

    return prev_row[-1]


def matrix_chain_multiplication(dimensions: List[int]) -> Tuple[int, str]:
    """
    Computes optimal matrix chain multiplication order.
    Returns (min_scalar_multiplications, formatted_parenthesization).
    """
    n = len(dimensions) - 1
    if n <= 0:
        return 0, ""

    m = [[0] * n for _ in range(n)]
    s = [[0] * n for _ in range(n)]

    for l in range(2, n + 1):
        for i in range(n - l + 1):
            j = i + l - 1
            m[i][j] = float("inf")
            for k in range(i, j):
                q = m[i][k] + m[k + 1][j] + dimensions[i] * dimensions[k + 1] * dimensions[j + 1]
                if q < m[i][j]:
                    m[i][j] = q
                    s[i][j] = k

    def build_parentheses(i: int, j: int) -> str:
        if i == j:
            return f"A{i + 1}"
        k = s[i][j]
        left = build_parentheses(i, k)
        right = build_parentheses(k + 1, j)
        return f"({left} x {right})"

    return int(m[0][n - 1]), build_parentheses(0, n - 1)
