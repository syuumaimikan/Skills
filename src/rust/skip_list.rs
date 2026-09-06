//! High-Performance Concurrent SkipList for In-Memory Indexing & LSM-Tree MemTable

use std::sync::atomic::{AtomicPtr, AtomicUsize, Ordering};
use std::ptr::null_mut;
use std::alloc::{alloc, Layout};

const MAX_LEVEL: usize = 16;
const P: f64 = 0.5;

struct Node<K, V> {
    key: K,
    value: V,
    level: usize,
    forward: [AtomicPtr<Node<K, V>>; MAX_LEVEL],
}

impl<K, V> Node<K, V> {
    fn new(key: K, value: V, level: usize) -> *mut Self {
        let node = Box::new(Self {
            key,
            value,
            level,
            forward: Default::default(),
        });
        Box::into_raw(node)
    }
}

pub struct SkipList<K: Ord + Clone, V: Clone> {
    head: *mut Node<K, V>,
    max_level: usize,
    length: AtomicUsize,
}

unsafe impl<K: Ord + Clone + Send, V: Clone + Send> Send for SkipList<K, V> {}
unsafe impl<K: Ord + Clone + Sync, V: Clone + Sync> Sync for SkipList<K, V> {}

impl<K: Ord + Clone + Default, V: Clone + Default> SkipList<K, V> {
    pub fn new() -> Self {
        let head = Node::new(K::default(), V::default(), MAX_LEVEL);
        Self {
            head,
            max_level: 1,
            length: AtomicUsize::new(0),
        }
    }

    fn random_level(&self) -> usize {
        let mut level = 1;
        while level < MAX_LEVEL && (rand_simple() < P) {
            level += 1;
        }
        level
    }

    pub fn insert(&mut self, key: K, value: V) {
        let mut update: [*mut Node<K, V>; MAX_LEVEL] = [null_mut(); MAX_LEVEL];
        let mut current = self.head;

        unsafe {
            for i in (0..self.max_level).rev() {
                while !(*current).forward[i].load(Ordering::Relaxed).is_null() {
                    let next = (*current).forward[i].load(Ordering::Relaxed);
                    if (*next).key < key {
                        current = next;
                    } else {
                        break;
                    }
                }
                update[i] = current;
            }

            let next = (*current).forward[0].load(Ordering::Relaxed);
            if !next.is_null() && (*next).key == key {
                // Update existing key
                (*next).value = value;
                return;
            }

            let new_level = self.random_level();
            if new_level > self.max_level {
                for i in self.max_level..new_level {
                    update[i] = self.head;
                }
                self.max_level = new_level;
            }

            let new_node = Node::new(key, value, new_level);
            for i in 0..new_level {
                let next_node = (*update[i]).forward[i].load(Ordering::Relaxed);
                (*new_node).forward[i].store(next_node, Ordering::Relaxed);
                (*update[i]).forward[i].store(new_node, Ordering::Release);
            }
        }

        self.length.fetch_add(1, Ordering::Relaxed);
    }

    pub fn get(&self, key: &K) -> Option<V> {
        let mut current = self.head;
        unsafe {
            for i in (0..self.max_level).rev() {
                while !(*current).forward[i].load(Ordering::Acquire).is_null() {
                    let next = (*current).forward[i].load(Ordering::Acquire);
                    if (*next).key < *key {
                        current = next;
                    } else {
                        break;
                    }
                }
            }

            let next = (*current).forward[0].load(Ordering::Acquire);
            if !next.is_null() && (*next).key == *key {
                return Some((*next).value.clone());
            }
        }
        None
    }

    pub fn len(&self) -> usize {
        self.length.load(Ordering::Relaxed)
    }

    pub fn is_empty(&self) -> bool {
        self.len() == 0
    }
}

// Simple xorshift pseudo random generator
fn rand_simple() -> f64 {
    static mut SEED: u64 = 88172645463325252;
    unsafe {
        SEED ^= SEED << 13;
        SEED ^= SEED >> 7;
        SEED ^= SEED << 17;
        (SEED as f64) / (u64::MAX as f64)
    }
}

impl<K: Ord + Clone, V: Clone> Drop for SkipList<K, V> {
    fn drop(&mut self) {
        unsafe {
            let mut current = self.head;
            while !current.is_null() {
                let next = (*current).forward[0].load(Ordering::Relaxed);
                let _ = Box::from_raw(current);
                current = next;
            }
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_skiplist_operations() {
        let mut list = SkipList::<i32, String>::new();
        list.insert(10, "ten".to_string());
        list.insert(5, "five".to_string());
        list.insert(20, "twenty".to_string());
        list.insert(15, "fifteen".to_string());

        assert_eq!(list.get(&10), Some("ten".to_string()));
        assert_eq!(list.get(&5), Some("five".to_string()));
        assert_eq!(list.get(&15), Some("fifteen".to_string()));
        assert_eq!(list.get(&999), None);
        assert_eq!(list.len(), 4);
    }
}
