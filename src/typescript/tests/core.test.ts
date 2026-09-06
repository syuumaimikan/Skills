import { test, describe } from 'node:test';
import assert from 'node:assert';
import { LRUCache, LFUCache } from '../data_structures/lru_lfu_cache.js';
import { RedBlackTree } from '../data_structures/red_black_tree.js';
import { Graph } from '../algorithms/graph_pathfinding.js';
import { ReactiveEventBus } from '../algorithms/reactive_event_bus.js';

describe('TypeScript Core Algorithms and Data Structures', () => {
  test('LRUCache eviction and retrieval', () => {
    const lru = new LRUCache<string, number>(2);
    lru.put('a', 1);
    lru.put('b', 2);
    assert.strictEqual(lru.get('a'), 1);

    lru.put('c', 3); // 'b' should be evicted because 'a' was recently accessed
    assert.strictEqual(lru.get('b'), undefined);
    assert.strictEqual(lru.get('c'), 3);
    assert.strictEqual(lru.get('a'), 1);
  });

  test('LFUCache eviction based on frequency', () => {
    const lfu = new LFUCache<string, number>(2);
    lfu.put('x', 10);
    lfu.put('y', 20);
    lfu.get('x'); // freq of x is 2, freq of y is 1

    lfu.put('z', 30); // y should be evicted (freq 1 < freq 2)
    assert.strictEqual(lfu.get('y'), undefined);
    assert.strictEqual(lfu.get('x'), 10);
    assert.strictEqual(lfu.get('z'), 30);
  });

  test('RedBlackTree insert, search, and ordering', () => {
    const tree = new RedBlackTree<number>();
    const values = [20, 15, 25, 10, 5, 1, 30, 22];
    for (const v of values) {
      tree.insert(v);
    }

    assert.strictEqual(tree.contains(15), true);
    assert.strictEqual(tree.contains(999), false);
    assert.strictEqual(tree.size(), 8);

    const sorted = tree.inOrderTraversal();
    const expected = [...values].sort((a, b) => a - b);
    assert.deepStrictEqual(sorted, expected);
  });

  test('Graph A* and Dijkstra pathfinding', () => {
    const graph = new Graph();
    graph.addNode({ id: 'A', x: 0, y: 0 });
    graph.addNode({ id: 'B', x: 1, y: 2 });
    graph.addNode({ id: 'C', x: 2, y: 0 });
    graph.addNode({ id: 'D', x: 3, y: 1 });

    graph.addEdge('A', 'B', 2.2);
    graph.addEdge('A', 'C', 2.0);
    graph.addEdge('B', 'D', 1.5);
    graph.addEdge('C', 'D', 1.8);

    const aStarRes = graph.aStarSearch('A', 'D');
    assert.ok(aStarRes);
    assert.strictEqual(aStarRes.path[0], 'A');
    assert.strictEqual(aStarRes.path[aStarRes.path.length - 1], 'D');

    const dijkstraRes = graph.dijkstra('A', 'D');
    assert.ok(dijkstraRes);
    assert.strictEqual(dijkstraRes.path[0], 'A');
    assert.strictEqual(dijkstraRes.path[dijkstraRes.path.length - 1], 'D');
  });

  test('ReactiveEventBus subscription and publishing', async () => {
    const bus = new ReactiveEventBus();
    let received = 0;

    const sub = bus.subscribe<number>('event:add', (val) => {
      received += val;
    });

    await bus.publish('event:add', 10);
    await bus.publish('event:add', 5);
    assert.strictEqual(received, 15);

    sub.unsubscribe();
    await bus.publish('event:add', 20);
    assert.strictEqual(received, 15);
  });
});
