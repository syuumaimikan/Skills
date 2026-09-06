package distributed

import (
	"fmt"
	"hash/fnv"
	"sort"
	"strconv"
	"sync"
)

// ConsistentHashRing implements consistent hashing with virtual nodes
type ConsistentHashRing struct {
	replicas int               // Number of virtual nodes per physical node
	ring     []uint32          // Sorted list of virtual node hashes
	nodeMap  map[uint32]string // Maps hash to physical node name
	mu       sync.RWMutex
}

// NewConsistentHashRing creates a new ring with the specified virtual node count
func NewConsistentHashRing(replicas int) *ConsistentHashRing {
	return &ConsistentHashRing{
		replicas: replicas,
		ring:     make([]uint32, 0),
		nodeMap:  make(map[uint32]string),
	}
}

func hashKey(key string) uint32 {
	hasher := fnv.New32a()
	_, _ = hasher.Write([]byte(key))
	return hasher.Sum32()
}

// AddNode adds a physical node and its virtual replicas to the ring
func (c *ConsistentHashRing) AddNode(node string) {
	c.mu.Lock()
	defer c.mu.Unlock()

	for i := 0; i < c.replicas; i++ {
		vNodeKey := node + "#" + strconv.Itoa(i)
		h := hashKey(vNodeKey)
		c.ring = append(c.ring, h)
		c.nodeMap[h] = node
	}
	sort.Slice(c.ring, func(i, j int) bool { return c.ring[i] < c.ring[j] })
}

// RemoveNode removes a physical node and its virtual replicas
func (c *ConsistentHashRing) RemoveNode(node string) {
	c.mu.Lock()
	defer c.mu.Unlock()

	newRing := make([]uint32, 0, len(c.ring))
	for _, h := range c.ring {
		if c.nodeMap[h] == node {
			delete(c.nodeMap, h)
		} else {
			newRing = append(newRing, h)
		}
	}
	c.ring = newRing
}

// GetNode routes a key to the closest physical node on the ring
func (c *ConsistentHashRing) GetNode(key string) (string, error) {
	c.mu.RLock()
	defer c.mu.RUnlock()

	if len(c.ring) == 0 {
		return "", fmt.Errorf("hash ring is empty")
	}

	h := hashKey(key)
	idx := sort.Search(len(c.ring), func(i int) bool {
		return c.ring[i] >= h
	})

	// Wrap around ring if key exceeds highest hash
	if idx == len(c.ring) {
		idx = 0
	}

	return c.nodeMap[c.ring[idx]], nil
}
