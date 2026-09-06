package distributed

import (
	"hash/fnv"
	"math"
	"sync"
)

// BloomFilter implements a thread-safe probabilistic set membership filter
type BloomFilter struct {
	bitset []uint64
	size   uint32
	k      uint32
	mu     sync.RWMutex
}

// NewBloomFilter creates an optimal Bloom Filter for expected elements N and false positive rate P
func NewBloomFilter(expectedElements uint32, falsePositiveRate float64) *BloomFilter {
	if falsePositiveRate <= 0 || falsePositiveRate >= 1 {
		falsePositiveRate = 0.01
	}

	// Optimal m = - (n * ln(p)) / (ln(2)^2)
	m := uint32(math.Ceil(-1 * (float64(expectedElements) * math.Log(falsePositiveRate)) / (math.Pow(math.Log(2), 2))))
	// Optimal k = (m / n) * ln(2)
	k := uint32(math.Ceil((float64(m) / float64(expectedElements)) * math.Log(2)))

	wordCount := (m + 63) / 64

	return &BloomFilter{
		bitset: make([]uint64, wordCount),
		size:   m,
		k:      k,
	}
}

func (bf *BloomFilter) getHashes(data string) []uint32 {
	hasher := fnv.New64a()
	_, _ = hasher.Write([]byte(data))
	h64 := hasher.Sum64()

	h1 := uint32(h64)
	h2 := uint32(h64 >> 32)

	hashes := make([]uint32, bf.k)
	for i := uint32(0); i < bf.k; i++ {
		// Double hashing scheme: g_i(x) = h1(x) + i * h2(x) mod m
		hashes[i] = (h1 + i*h2) % bf.size
	}
	return hashes
}

// Add inserts an item into the Bloom Filter
func (bf *BloomFilter) Add(item string) {
	hashes := bf.getHashes(item)

	bf.mu.Lock()
	defer bf.mu.Unlock()

	for _, pos := range hashes {
		wordIdx := pos / 64
		bitIdx := pos % 64
		bf.bitset[wordIdx] |= (1 << bitIdx)
	}
}

// Contains checks whether an item might be in the set (true) or definitely is not (false)
func (bf *BloomFilter) Contains(item string) bool {
	hashes := bf.getHashes(item)

	bf.mu.RLock()
	defer bf.mu.RUnlock()

	for _, pos := range hashes {
		wordIdx := pos / 64
		bitIdx := pos % 64
		if (bf.bitset[wordIdx] & (1 << bitIdx)) == 0 {
			return false
		}
	}
	return true
}
