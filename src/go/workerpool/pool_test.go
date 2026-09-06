package workerpool

import (
	"context"
	"sync/atomic"
	"testing"
	"time"
)

func TestWorkerPoolExecution(t *testing.T) {
	pool := NewWorkerPool(4, 50)
	var counter int64

	taskCount := 100
	for i := 0; i < taskCount; i++ {
		pool.Submit(func(ctx context.Context) {
			time.Sleep(1 * time.Millisecond)
			atomic.AddInt64(&counter, 1)
		})
	}

	time.Sleep(100 * time.Millisecond)
	pool.Stop()

	if atomic.LoadInt64(&counter) != int64(taskCount) {
		t.Errorf("Expected counter to be %d, got %d", taskCount, counter)
	}
}
