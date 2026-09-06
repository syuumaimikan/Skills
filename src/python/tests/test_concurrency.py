import asyncio
import unittest
from src.python.concurrency.async_pipeline import TokenBucketRateLimiter, AsyncWorkerPool


class TestConcurrency(unittest.TestCase):
    def test_token_bucket(self):
        async def run_test():
            limiter = TokenBucketRateLimiter(capacity=2.0, refill_rate=10.0)
            self.assertTrue(await limiter.acquire(1.0))
            self.assertTrue(await limiter.acquire(1.0))
            self.assertFalse(await limiter.acquire(1.0))
            await asyncio.sleep(0.15)
            self.assertTrue(await limiter.acquire(1.0))

        asyncio.run(run_test())

    def test_async_worker_pool(self):
        async def run_test():
            pool = AsyncWorkerPool(worker_count=2, max_queue_size=10)
            await pool.start()

            async def sample_task(val: int):
                await asyncio.sleep(0.01)
                return val * 2

            for i in range(4):
                await pool.submit(sample_task, i)

            await pool.shutdown()
            self.assertEqual(sorted(pool.results), [0, 2, 4, 6])

        asyncio.run(run_test())


if __name__ == "__main__":
    unittest.main()
