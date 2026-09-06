package com.skills.core.concurrency

import java.util.concurrent.atomic.AtomicLong
import java.util.concurrent.ConcurrentLinkedQueue

/**
 * High-Throughput Reactive Pipeline & Batch Dispatcher
 */
class BatchProcessor<T, R>(
    private val batchSize: Int = 50,
    private val transform: (List<T>) -> List<R>
) {
    private val queue = ConcurrentLinkedQueue<T>()
    private val processedCount = AtomicLong(0)

    fun submit(item: T) {
        queue.offer(item)
    }

    fun submitAll(items: Collection<T>) {
        items.forEach { queue.offer(it) }
    }

    fun flushBatch(): List<R> {
        val batch = mutableListOf<T>()
        while (batch.size < batchSize) {
            val item = queue.poll() ?: break
            batch.add(item)
        }

        if (batch.isEmpty()) return emptyList()

        val results = transform(batch)
        processedCount.addAndGet(batch.size.toLong())
        return results
    }

    fun pendingCount(): Int = queue.size

    fun totalProcessed(): Long = processedCount.get()
}
