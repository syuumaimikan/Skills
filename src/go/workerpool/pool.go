package workerpool

import (
	"context"
	"sync"
)

// Task represents a unit of work
type Task func(ctx context.Context)

// WorkerPool manages a fixed pool of goroutines executing tasks
type WorkerPool struct {
	maxWorkers int
	taskQueue  chan Task
	wg         sync.WaitGroup
	ctx        context.Context
	cancel     context.CancelFunc
}

// NewWorkerPool initializes and starts the worker pool
func NewWorkerPool(maxWorkers, queueCapacity int) *WorkerPool {
	ctx, cancel := context.WithCancel(context.Background())
	pool := &WorkerPool{
		maxWorkers: maxWorkers,
		taskQueue:  make(chan Task, queueCapacity),
		ctx:        ctx,
		cancel:     cancel,
	}

	pool.start()
	return pool
}

func (p *WorkerPool) start() {
	for i := 0; i < p.maxWorkers; i++ {
		p.wg.Add(1)
		go func() {
			defer p.wg.Done()
			for {
				select {
				case <-p.ctx.Done():
					// Drain remaining tasks before quitting
					for {
						select {
						case task, ok := <-p.taskQueue:
							if !ok {
								return
							}
							task(p.ctx)
						default:
							return
						}
					}
				case task, ok := <-p.taskQueue:
					if !ok {
						return
					}
					task(p.ctx)
				}
			}
		}()
	}
}

// Submit queues a task for execution
func (p *WorkerPool) Submit(task Task) bool {
	select {
	case <-p.ctx.Done():
		return false
	case p.taskQueue <- task:
		return true
	}
}

// Stop gracefully shuts down the worker pool
func (p *WorkerPool) Stop() {
	p.cancel()
	close(p.taskQueue)
	p.wg.Wait()
}
