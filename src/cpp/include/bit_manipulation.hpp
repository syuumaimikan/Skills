#pragma once
#include <cstdint>
#include <vector>
#include <bit>

namespace skills::bits {

/**
 * Binary Indexed Tree (Fenwick Tree) for O(log N) point updates and range sum queries
 */
class FenwickTree {
private:
    std::vector<int64_t> tree_;
    size_t size_;

public:
    explicit FenwickTree(size_t n) : tree_(n + 1, 0), size_(n) {}

    void add(size_t idx, int64_t delta) {
        for (++idx; idx <= size_; idx += idx & -idx) {
            tree_[idx] += delta;
        }
    }

    int64_t query(size_t idx) const {
        int64_t sum = 0;
        for (++idx; idx > 0; idx -= idx & -idx) {
            sum += tree_[idx];
        }
        return sum;
    }

    int64_t queryRange(size_t left, size_t right) const {
        if (left > right) return 0;
        return query(right) - (left > 0 ? query(left - 1) : 0);
    }
};

/**
 * Fast Bitwise Utilities
 */
inline uint32_t popcount(uint64_t x) noexcept {
    return static_cast<uint32_t>(std::popcount(x));
}

inline uint32_t count_trailing_zeros(uint64_t x) noexcept {
    return static_cast<uint32_t>(std::countr_zero(x));
}

} // namespace skills::bits
