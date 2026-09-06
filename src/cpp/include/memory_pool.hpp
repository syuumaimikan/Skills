#pragma once
#include <cstddef>
#include <vector>
#include <utility>
#include <stdexcept>

namespace skills::memory {

/**
 * High-Performance Fixed-Size Slab / Chunk Memory Pool Allocator
 * Zero runtime fragmentation and O(1) allocation/deallocation.
 */
template <typename T, size_t BlockSize = 1024>
class MemoryPool {
private:
    union Node {
        T element;
        Node* next;
        Node() {}
        ~Node() {}
    };

    struct Block {
        Node* memory;
        Block* next;
        Block() : memory(static_cast<Node*>(::operator new(BlockSize * sizeof(Node)))), next(nullptr) {}
        ~Block() { ::operator delete(memory); }
    };

    Block* currentBlock_ = nullptr;
    Node* freeList_ = nullptr;
    size_t allocatedCount_ = 0;

public:
    MemoryPool() {
        allocateNewBlock();
    }

    ~MemoryPool() {
        while (currentBlock_) {
            Block* next = currentBlock_->next;
            delete currentBlock_;
            currentBlock_ = next;
        }
    }

    MemoryPool(const MemoryPool&) = delete;
    MemoryPool& operator=(const MemoryPool&) = delete;

    template <typename... Args>
    T* allocate(Args&&... args) {
        if (!freeList_) {
            allocateNewBlock();
        }
        Node* node = freeList_;
        freeList_ = freeList_->next;
        allocatedCount_++;
        return new (&node->element) T(std::forward<Args>(args)...);
    }

    void deallocate(T* ptr) {
        if (!ptr) return;
        ptr->~T();
        Node* node = reinterpret_cast<Node*>(ptr);
        node->next = freeList_;
        freeList_ = node;
        allocatedCount_--;
    }

    size_t size() const noexcept {
        return allocatedCount_;
    }

private:
    void allocateNewBlock() {
        Block* newBlock = new Block();
        newBlock->next = currentBlock_;
        currentBlock_ = newBlock;

        for (size_t i = 0; i < BlockSize - 1; ++i) {
            newBlock->memory[i].next = &newBlock->memory[i + 1];
        }
        newBlock->memory[BlockSize - 1].next = freeList_;
        freeList_ = &newBlock->memory[0];
    }
};

} // namespace skills::memory
