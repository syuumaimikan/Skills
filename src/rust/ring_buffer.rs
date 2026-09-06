//! High-Performance Single-Producer Single-Consumer (SPSC) Lock-Free Ring Buffer

use std::cell::UnsafeCell;
use std::mem::MaybeUninit;
use std::sync::atomic::{AtomicUsize, Ordering};
use std::sync::Arc;

pub struct SpscRingBuffer<T> {
    buffer: Vec<UnsafeCell<MaybeUninit<T>>>,
    capacity: usize,
    mask: usize,
    head: AtomicUsize, // Written by Producer, read by Consumer
    tail: AtomicUsize, // Written by Consumer, read by Producer
}

unsafe impl<T: Send> Send for SpscRingBuffer<T> {}
unsafe impl<T: Send> Sync for SpscRingBuffer<T> {}

impl<T> SpscRingBuffer<T> {
    pub fn new(capacity: usize) -> Self {
        assert!(capacity > 0, "Capacity must be positive");
        let power_of_two_cap = capacity.next_power_of_two();
        let mut buffer = Vec::with_capacity(power_of_two_cap);
        for _ in 0..power_of_two_cap {
            buffer.push(UnsafeCell::new(MaybeUninit::uninit()));
        }

        Self {
            buffer,
            capacity: power_of_two_cap,
            mask: power_of_two_cap - 1,
            head: AtomicUsize::new(0),
            tail: AtomicUsize::new(0),
        }
    }

    /// Push an element to the ring buffer. Returns Err(item) if full.
    pub fn push(&self, item: T) -> Result<(), T> {
        let head = self.head.load(Ordering::Relaxed);
        let tail = self.tail.load(Ordering::Acquire);

        if head.wrapping_sub(tail) >= self.capacity {
            return Err(item); // Buffer full
        }

        let slot = &self.buffer[head & self.mask];
        unsafe {
            (*slot.get()).write(item);
        }

        self.head.store(head.wrapping_add(1), Ordering::Release);
        Ok(())
    }

    /// Pop an element from the ring buffer. Returns None if empty.
    pub fn pop(&self) -> Option<T> {
        let tail = self.tail.load(Ordering::Relaxed);
        let head = self.head.load(Ordering::Acquire);

        if tail == head {
            return None; // Buffer empty
        }

        let slot = &self.buffer[tail & self.mask];
        let item = unsafe { (*slot.get()).assume_init_read() };

        self.tail.store(tail.wrapping_add(1), Ordering::Release);
        Some(item)
    }

    pub fn len(&self) -> usize {
        let head = self.head.load(Ordering::Acquire);
        let tail = self.tail.load(Ordering::Acquire);
        head.wrapping_sub(tail)
    }

    pub fn is_empty(&self) -> bool {
        self.len() == 0
    }
}

impl<T> Drop for SpscRingBuffer<T> {
    fn drop(&mut self) {
        while self.pop().is_some() {}
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::thread;

    #[test]
    fn test_spsc_basic() {
        let rb = SpscRingBuffer::<i32>::new(4);
        assert_eq!(rb.push(1), Ok(()));
        assert_eq!(rb.push(2), Ok(()));
        assert_eq!(rb.push(3), Ok(()));
        assert_eq!(rb.push(4), Ok(()));
        assert!(rb.push(5).is_err()); // Full

        assert_eq!(rb.pop(), Some(1));
        assert_eq!(rb.pop(), Some(2));
        assert_eq!(rb.push(5), Ok(()));
        assert_eq!(rb.pop(), Some(3));
        assert_eq!(rb.pop(), Some(4));
        assert_eq!(rb.pop(), Some(5));
        assert_eq!(rb.pop(), None);
    }

    #[test]
    fn test_spsc_multithreaded() {
        let rb = Arc::new(SpscRingBuffer::<usize>::new(1024));
        let rb_producer = Arc::clone(&rb);
        let rb_consumer = Arc::clone(&rb);

        let total = 50_000;
        let producer = thread::spawn(move || {
            for i in 0..total {
                while rb_producer.push(i).is_err() {
                    std::hint::spin_loop();
                }
            }
        });

        let consumer = thread::spawn(move || {
            let mut sum = 0;
            for _ in 0..total {
                loop {
                    if let Some(val) = rb_consumer.pop() {
                        sum += val;
                        break;
                    }
                    std::hint::spin_loop();
                }
            }
            sum
        });

        producer.join().unwrap();
        let sum = consumer.join().unwrap();
        let expected_sum: usize = (0..total).sum();
        assert_eq!(sum, expected_sum);
    }
}
