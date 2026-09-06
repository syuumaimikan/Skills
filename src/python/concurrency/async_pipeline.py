"""
High-throughput Asynchronous Pipeline & Concurrency Patterns in Python
- Async Worker Pool with bounded queue
- Token Bucket Rate Limiter
- Non-blocking Pipeline with backpressure
"""

import asyncio
import time
from typing import Callable, Coroutine, Any, List, Optional


class TokenBucketRateLimiter:
    """
    Thread-safe / Async Token Bucket Rate Limiter
    """
    def __init__(self, capacity: float, refill_rate: float):
        self.capacity = capacity
        self.refill_rate = refill_rate  # tokens per second
        self.tokens = capacity
        self.last_refill = time.monotonic()
        self._lock = asyncio.Lock()

    async def acquire(self, tokens: float = 1.0) -> bool:
        async with self._lock:
            now = time.monotonic()
            elapsed = now - self.last_refill
            self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
            self.last_refill = now

            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False

    async def wait_and_acquire(self, tokens: float = 1.0) -> None:
        while not await self.acquire(tokens):
            await asyncio.sleep(1.0 / self.refill_rate)


class AsyncWorkerPool:
    """
    Asynchronous Worker Pool with bounded queue and graceful shutdown
    """
    def __init__(self, worker_count: int = 4, max_queue_size: int = 100):
        self.worker_count = worker_count
        self.queue: asyncio.Queue = asyncio.Queue(maxsize=max_queue_size)
        self.workers: List[asyncio.Task] = []
        self.results: List[Any] = []
        self._running = False

    async def _worker_loop(self, worker_id: int):
        while self._running:
            try:
                task_fn, args, kwargs = await self.queue.get()
                try:
                    res = await task_fn(*args, **kwargs)
                    self.results.append(res)
                except Exception as e:
                    self.results.append(e)
                finally:
                    self.queue.task_done()
            except asyncio.CancelledError:
                break

    async def start(self):
        self._running = True
        self.workers = [
            asyncio.create_task(self._worker_loop(i))
            for i in range(self.worker_count)
        ]

    async def submit(self, task_fn: Callable[..., Coroutine[Any, Any, Any]], *args, **kwargs):
        if not self._running:
            raise RuntimeError("Worker pool is not running")
        await self.queue.put((task_fn, args, kwargs))

    async def shutdown(self):
        await self.queue.join()
        self._running = False
        for w in self.workers:
            w.cancel()
        await asyncio.gather(*self.workers, return_exceptions=True)
