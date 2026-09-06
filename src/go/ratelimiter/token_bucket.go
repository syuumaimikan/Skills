package ratelimiter

import (
	"sync"
	"time"
)

// TokenBucket implements a concurrent-safe Token Bucket rate limiter
type TokenBucket struct {
	capacity   float64
	refillRate float64 // Tokens per second
	tokens     float64
	lastRefill time.Time
	mu         sync.Mutex
}

// NewTokenBucket creates a new TokenBucket rate limiter
func NewTokenBucket(capacity, refillRate float64) *TokenBucket {
	return &TokenBucket{
		capacity:   capacity,
		refillRate: refillRate,
		tokens:     capacity,
		lastRefill: time.Now(),
	}
}

// Allow checks if the requested tokens are available and consumes them
func (tb *TokenBucket) Allow(tokens float64) bool {
	tb.mu.Lock()
	defer tb.mu.Unlock()

	now := time.Now()
	elapsed := now.Sub(tb.lastRefill).Seconds()
	tb.tokens += elapsed * tb.refillRate
	if tb.tokens > tb.capacity {
		tb.tokens = tb.capacity
	}
	tb.lastRefill = now

	if tb.tokens >= tokens {
		tb.tokens -= tokens
		return true
	}
	return false
}
