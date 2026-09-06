//! Polyglot Skills Core - Rust High Performance Library
//! 
//! High-throughput primitives designed for maximum efficiency:
//! - Lock-free bounded Ring Buffer (SPSC)
//! - Concurrent Thread Pool with Work-Stealing
//! - Vectorized / SIMD Math & Matrix Multiplications

pub mod ring_buffer;
pub mod thread_pool;
pub mod simd_math;
pub mod skip_list;

pub use ring_buffer::SpscRingBuffer;
pub use thread_pool::ThreadPool;
pub use simd_math::{dot_product, matrix_multiply_2d};
pub use skip_list::SkipList;
