import asyncio
import pytest
from src.python.concurrency.async_pipeline import TokenBucketRateLimiter, AsyncWorkerPool


@pytest.mark.asyncio
async def test_token_bucket():
    limiter = TokenBucketRateLimiter(capacity=2.0, refill_rate=10.0)
    assert await limiter.acquire(1.0) is True
    assert await limiter.acquire(1.0) is True
    # Capacity exhausted immediately
    assert await limiter.acquire(1.0) is False
    await asyncio.sleep(0.15)
    # Refilled tokens
    assert await limiter.acquire(1.0) is True


@pytest.mark.asyncio
async def test_async_worker_pool():
    pool = AsyncWorkerPool(worker_count=2, max_queue_size=10)
    await pool.start()

    async def sample_task(val: int):
        await asyncio.sleep(0.01)
        return val * 2

    for i in range(4):
        await pool.submit(sample_task, i)

    await pool.shutdown()
    assert sorted(pool.results) == [0, 2, 4, 6]
