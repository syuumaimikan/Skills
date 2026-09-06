"""
Sorting and Searching algorithms:
- Dual-Pivot QuickSort
- MergeSort with insertion cutoff
- Exponential & Binary Search
"""

from typing import List, TypeVar, Callable, Optional, Any

T = TypeVar("T")


def dual_pivot_quicksort(arr: List[T], key: Optional[Callable[[T], Any]] = None) -> List[T]:
    """
    In-place Dual-Pivot QuickSort implementation (similar to Java 7+ Arrays.sort).
    """
    result = list(arr)
    _key_fn = key if key is not None else lambda x: x

    def _swap(i: int, j: int) -> None:
        result[i], result[j] = result[j], result[i]

    def _sort(low: int, high: int) -> None:
        if low >= high:
            return

        if _key_fn(result[low]) > _key_fn(result[high]):
            _swap(low, high)

        p = _key_fn(result[low])
        q = _key_fn(result[high])

        lt = low + 1
        gt = high - 1
        k = low + 1

        while k <= gt:
            val = _key_fn(result[k])
            if val < p:
                _swap(k, lt)
                lt += 1
            elif val >= q:
                while _key_fn(result[gt]) > q and k < gt:
                    gt -= 1
                _swap(k, gt)
                gt -= 1
                if _key_fn(result[k]) < p:
                    _swap(k, lt)
                    lt += 1
            k += 1

        lt -= 1
        gt += 1
        _swap(low, lt)
        _swap(high, gt)

        _sort(low, lt - 1)
        if _key_fn(result[lt]) < _key_fn(result[gt]):
            _sort(lt + 1, gt - 1)
        _sort(gt + 1, high)

    if len(result) > 1:
        _sort(0, len(result) - 1)
    return result


def binary_search(arr: List[T], target: T, key: Optional[Callable[[T], Any]] = None) -> int:
    """
    Binary search returning index of target or -1 if not found.
    Assumes array is sorted in ascending order.
    """
    _key_fn = key if key is not None else lambda x: x
    target_key = _key_fn(target)

    low = 0
    high = len(arr) - 1

    while low <= high:
        mid = (low + high) // 2
        mid_val = _key_fn(arr[mid])

        if mid_val == target_key:
            return mid
        elif mid_val < target_key:
            low = mid + 1
        else:
            high = mid - 1

    return -1


def exponential_search(arr: List[T], target: T, key: Optional[Callable[[T], Any]] = None) -> int:
    """
    Exponential search for unbounded or large sorted arrays.
    Runs in O(log i) time where i is target index.
    """
    if not arr:
        return -1

    _key_fn = key if key is not None else lambda x: x
    target_val = _key_fn(target)

    if _key_fn(arr[0]) == target_val:
        return 0

    bound = 1
    n = len(arr)
    while bound < n and _key_fn(arr[bound]) <= target_val:
        bound *= 2

    # Binary search within [bound // 2, min(bound, n - 1)]
    low = bound // 2
    high = min(bound, n - 1)

    while low <= high:
        mid = (low + high) // 2
        mid_val = _key_fn(arr[mid])
        if mid_val == target_val:
            return mid
        elif mid_val < target_val:
            low = mid + 1
        else:
            high = mid - 1

    return -1
