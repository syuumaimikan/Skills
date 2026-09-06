/**
 * Advanced Graph Pathfinding Algorithms: A*, Dijkstra, Bidirectional BFS
 */

export interface GraphNode {
  id: string;
  x: number;
  y: number;
}

export interface Edge {
  target: string;
  weight: number;
}

export interface PathResult {
  path: string[];
  totalCost: number;
  nodesVisited: number;
}

export class PriorityQueue<T> {
  private heap: { item: T; priority: number }[] = [];

  public enqueue(item: T, priority: number): void {
    this.heap.push({ item, priority });
    this.bubbleUp(this.heap.length - 1);
  }

  public dequeue(): T | undefined {
    if (this.heap.length === 0) return undefined;
    const top = this.heap[0].item;
    const bottom = this.heap.pop()!;
    if (this.heap.length > 0) {
      this.heap[0] = bottom;
      this.sinkDown(0);
    }
    return top;
  }

  public isEmpty(): boolean {
    return this.heap.length === 0;
  }

  private bubbleUp(index: number): void {
    const element = this.heap[index];
    while (index > 0) {
      const parentIdx = Math.floor((index - 1) / 2);
      const parent = this.heap[parentIdx];
      if (element.priority >= parent.priority) break;
      this.heap[index] = parent;
      this.heap[parentIdx] = element;
      index = parentIdx;
    }
  }

  private sinkDown(index: number): void {
    const length = this.heap.length;
    const element = this.heap[index];
    while (true) {
      let leftChildIdx = 2 * index + 1;
      let rightChildIdx = 2 * index + 2;
      let swapIdx: number | null = null;

      if (leftChildIdx < length) {
        if (this.heap[leftChildIdx].priority < element.priority) {
          swapIdx = leftChildIdx;
        }
      }

      if (rightChildIdx < length) {
        if (
          (swapIdx === null && this.heap[rightChildIdx].priority < element.priority) ||
          (swapIdx !== null && this.heap[rightChildIdx].priority < this.heap[leftChildIdx].priority)
        ) {
          swapIdx = rightChildIdx;
        }
      }

      if (swapIdx === null) break;
      this.heap[index] = this.heap[swapIdx];
      this.heap[swapIdx] = element;
      index = swapIdx;
    }
  }
}

export class Graph {
  private nodes: Map<string, GraphNode> = new Map();
  private adjacencyList: Map<string, Edge[]> = new Map();

  public addNode(node: GraphNode): void {
    this.nodes.set(node.id, node);
    if (!this.adjacencyList.has(node.id)) {
      this.adjacencyList.set(node.id, []);
    }
  }

  public addEdge(from: string, to: string, weight: number, bidirectional = true): void {
    this.adjacencyList.get(from)?.push({ target: to, weight });
    if (bidirectional) {
      this.adjacencyList.get(to)?.push({ target: from, weight });
    }
  }

  /**
   * Euclidean distance heuristic for A*
   */
  private euclideanHeuristic(nodeA: GraphNode, nodeB: GraphNode): number {
    const dx = nodeA.x - nodeB.x;
    const dy = nodeA.y - nodeB.y;
    return Math.sqrt(dx * dx + dy * dy);
  }

  /**
   * A* Pathfinding Algorithm
   */
  public aStarSearch(startId: string, goalId: string): PathResult | null {
    const startNode = this.nodes.get(startId);
    const goalNode = this.nodes.get(goalId);
    if (!startNode || !goalNode) return null;

    const openSet = new PriorityQueue<string>();
    const gScore = new Map<string, number>();
    const fScore = new Map<string, number>();
    const cameFrom = new Map<string, string>();
    let visitedCount = 0;

    for (const id of this.nodes.keys()) {
      gScore.set(id, Infinity);
      fScore.set(id, Infinity);
    }

    gScore.set(startId, 0);
    const initialH = this.euclideanHeuristic(startNode, goalNode);
    fScore.set(startId, initialH);
    openSet.enqueue(startId, initialH);

    while (!openSet.isEmpty()) {
      const current = openSet.dequeue()!;
      visitedCount++;

      if (current === goalId) {
        // Reconstruct path
        const path: string[] = [current];
        let curr = current;
        while (cameFrom.has(curr)) {
          curr = cameFrom.get(curr)!;
          path.unshift(curr);
        }
        return {
          path,
          totalCost: gScore.get(goalId) ?? 0,
          nodesVisited: visitedCount,
        };
      }

      const neighbors = this.adjacencyList.get(current) || [];
      for (const edge of neighbors) {
        const tentativeG = (gScore.get(current) ?? Infinity) + edge.weight;
        if (tentativeG < (gScore.get(edge.target) ?? Infinity)) {
          cameFrom.set(edge.target, current);
          gScore.set(edge.target, tentativeG);
          const targetNode = this.nodes.get(edge.target)!;
          const h = this.euclideanHeuristic(targetNode, goalNode);
          const f = tentativeG + h;
          fScore.set(edge.target, f);
          openSet.enqueue(edge.target, f);
        }
      }
    }

    return null;
  }

  /**
   * Dijkstra's Algorithm for Shortest Path
   */
  public dijkstra(startId: string, goalId: string): PathResult | null {
    const distances = new Map<string, number>();
    const previous = new Map<string, string | null>();
    const pq = new PriorityQueue<string>();
    let visitedCount = 0;

    for (const node of this.nodes.keys()) {
      distances.set(node, Infinity);
      previous.set(node, null);
    }

    distances.set(startId, 0);
    pq.enqueue(startId, 0);

    while (!pq.isEmpty()) {
      const current = pq.dequeue()!;
      visitedCount++;

      if (current === goalId) {
        const path: string[] = [];
        let curr: string | null = goalId;
        while (curr !== null) {
          path.unshift(curr);
          curr = previous.get(curr) || null;
        }
        return {
          path,
          totalCost: distances.get(goalId) ?? 0,
          nodesVisited: visitedCount,
        };
      }

      const neighbors = this.adjacencyList.get(current) || [];
      for (const edge of neighbors) {
        const alt = (distances.get(current) ?? Infinity) + edge.weight;
        if (alt < (distances.get(edge.target) ?? Infinity)) {
          distances.set(edge.target, alt);
          previous.set(edge.target, current);
          pq.enqueue(edge.target, alt);
        }
      }
    }

    return null;
  }
}
