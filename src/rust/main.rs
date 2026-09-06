use skills_core::{dot_product, ThreadPool, SpscRingBuffer};
use std::time::Instant;

fn main() {
    println!("=== Polyglot Skills Core - Rust Engine Benchmark ===");

    // Benchmark 1: SIMD Dot Product
    let size = 1_000_000;
    let v1 = vec![1.001f32; size];
    let v2 = vec![0.999f32; size];

    let start = Instant::now();
    let dot = dot_product(&v1, &v2);
    let duration = start.elapsed();
    println!("Vector Dot Product (1M f32): result = {:.4}, elapsed = {:?}", dot, duration);

    // Benchmark 2: ThreadPool Task Execution
    let pool = ThreadPool::new(8);
    let start = Instant::now();
    for _ in 0..10_000 {
        pool.execute(|| {
            let _ = 1 + 1;
        });
    }
    drop(pool);
    println!("ThreadPool (10,000 tasks): elapsed = {:?}", start.elapsed());

    // Benchmark 3: Lock-free SPSC Ring Buffer
    let rb = SpscRingBuffer::<usize>::new(1024);
    let start = Instant::now();
    for i in 0..100_000 {
        let _ = rb.push(i);
        let _ = rb.pop();
    }
    println!("SPSC RingBuffer (100k push/pop): elapsed = {:?}", start.elapsed());
}
