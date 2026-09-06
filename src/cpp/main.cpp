#include <iostream>
#include <chrono>
#include <vector>
#include "memory_pool.hpp"
#include "bit_manipulation.hpp"

struct Particle {
    float x, y, z;
    float vx, vy, vz;
    int id;
};

int main() {
    std::cout << "=== Polyglot Skills Core - C++ Engine Benchmark ===" << std::endl;

    // Test 1: Fenwick Tree
    skills::bits::FenwickTree bit(1000);
    for (size_t i = 0; i < 100; ++i) {
        bit.add(i, static_cast<int64_t>(i + 1));
    }
    std::cout << "Fenwick Tree Range Sum [0, 99]: " << bit.queryRange(0, 99) << std::endl;

    // Test 2: MemoryPool Benchmark vs Standard Allocator
    constexpr size_t N = 1000000;
    
    // Custom MemoryPool
    auto start = std::chrono::high_resolution_clock::now();
    skills::memory::MemoryPool<Particle, 4096> pool;
    std::vector<Particle*> particles;
    particles.reserve(N);

    for (size_t i = 0; i < N; ++i) {
        particles.push_back(pool.allocate());
    }
    for (auto* p : particles) {
        pool.deallocate(p);
    }
    auto pool_elapsed = std::chrono::duration_cast<std::chrono::microseconds>(
        std::chrono::high_resolution_clock::now() - start
    ).count();

    std::cout << "Custom MemoryPool 1M alloc/dealloc: " << pool_elapsed / 1000.0 << " ms" << std::endl;
    return 0;
}
