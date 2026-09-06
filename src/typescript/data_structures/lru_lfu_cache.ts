/**
 * High-performance Cache Implementations: LRU (Least Recently Used) and LFU (Least Frequently Used)
 * Time Complexity: O(1) Get and Put
 */

class DoublyLinkedListNode<K, V> {
  key: K;
  value: V;
  frequency: number;
  prev: DoublyLinkedListNode<K, V> | null = null;
  next: DoublyLinkedListNode<K, V> | null = null;

  constructor(key: K, value: V, frequency = 1) {
    this.key = key;
    this.value = value;
    this.frequency = frequency;
  }
}

/**
 * LRU Cache (Least Recently Used) with O(1) get & put
 */
export class LRUCache<K, V> {
  private capacity: number;
  private cache: Map<K, DoublyLinkedListNode<K, V>> = new Map();
  private head: DoublyLinkedListNode<K, V>;
  private tail: DoublyLinkedListNode<K, V>;

  constructor(capacity: number) {
    if (capacity <= 0) {
      throw new Error("Capacity must be greater than 0");
    }
    this.capacity = capacity;
    // Dummy sentinel nodes
    this.head = new DoublyLinkedListNode<K, V>(null as any, null as any);
    this.tail = new DoublyLinkedListNode<K, V>(null as any, null as any);
    this.head.next = this.tail;
    this.tail.prev = this.head;
  }

  public get(key: K): V | undefined {
    const node = this.cache.get(key);
    if (!node) return undefined;

    this.moveToHead(node);
    return node.value;
  }

  public put(key: K, value: V): void {
    const existing = this.cache.get(key);
    if (existing) {
      existing.value = value;
      this.moveToHead(existing);
      return;
    }

    if (this.cache.size >= this.capacity) {
      const removed = this.removeTail();
      if (removed) {
        this.cache.delete(removed.key);
      }
    }

    const newNode = new DoublyLinkedListNode(key, value);
    this.cache.set(key, newNode);
    this.addToHead(newNode);
  }

  public size(): number {
    return this.cache.size;
  }

  public clear(): void {
    this.cache.clear();
    this.head.next = this.tail;
    this.tail.prev = this.head;
  }

  private addToHead(node: DoublyLinkedListNode<K, V>): void {
    node.prev = this.head;
    node.next = this.head.next;
    if (this.head.next) {
      this.head.next.prev = node;
    }
    this.head.next = node;
  }

  private removeNode(node: DoublyLinkedListNode<K, V>): void {
    if (node.prev) node.prev.next = node.next;
    if (node.next) node.next.prev = node.prev;
  }

  private moveToHead(node: DoublyLinkedListNode<K, V>): void {
    this.removeNode(node);
    this.addToHead(node);
  }

  private removeTail(): DoublyLinkedListNode<K, V> | null {
    const last = this.tail.prev;
    if (last && last !== this.head) {
      this.removeNode(last);
      return last;
    }
    return null;
  }
}

/**
 * LFU Cache (Least Frequently Used) with O(1) average time complexity
 */
export class LFUCache<K, V> {
  private capacity: number;
  private minFreq: number = 0;
  private keyMap: Map<K, DoublyLinkedListNode<K, V>> = new Map();
  private freqMap: Map<number, Set<DoublyLinkedListNode<K, V>>> = new Map();

  constructor(capacity: number) {
    if (capacity <= 0) {
      throw new Error("Capacity must be greater than 0");
    }
    this.capacity = capacity;
  }

  public get(key: K): V | undefined {
    const node = this.keyMap.get(key);
    if (!node) return undefined;
    this.updateFrequency(node);
    return node.value;
  }

  public put(key: K, value: V): void {
    if (this.capacity === 0) return;

    const existing = this.keyMap.get(key);
    if (existing) {
      existing.value = value;
      this.updateFrequency(existing);
      return;
    }

    if (this.keyMap.size >= this.capacity) {
      const minList = this.freqMap.get(this.minFreq);
      if (minList && minList.size > 0) {
        const evictNode = minList.values().next().value;
        if (evictNode) {
          minList.delete(evictNode);
          this.keyMap.delete(evictNode.key);
        }
      }
    }

    const newNode = new DoublyLinkedListNode(key, value, 1);
    this.keyMap.set(key, newNode);
    if (!this.freqMap.has(1)) {
      this.freqMap.set(1, new Set());
    }
    this.freqMap.get(1)!.add(newNode);
    this.minFreq = 1;
  }

  private updateFrequency(node: DoublyLinkedListNode<K, V>): void {
    const oldFreq = node.frequency;
    const oldList = this.freqMap.get(oldFreq);
    if (oldList) {
      oldList.delete(node);
      if (oldList.size === 0 && this.minFreq === oldFreq) {
        this.minFreq++;
      }
    }

    node.frequency++;
    if (!this.freqMap.has(node.frequency)) {
      this.freqMap.set(node.frequency, new Set());
    }
    this.freqMap.get(node.frequency)!.add(node);
  }

  public size(): number {
    return this.keyMap.size;
  }
}
