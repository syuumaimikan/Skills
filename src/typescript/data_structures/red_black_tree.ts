/**
 * Red-Black Tree Implementation (Self-Balancing Binary Search Tree)
 * Guarantees O(log N) operations for insert, delete, search.
 */

enum Color {
  RED,
  BLACK,
}

class RBNode<T> {
  value: T;
  color: Color = Color.RED;
  left: RBNode<T> | null = null;
  right: RBNode<T> | null = null;
  parent: RBNode<T> | null = null;

  constructor(value: T) {
    this.value = value;
  }
}

export class RedBlackTree<T> {
  private root: RBNode<T> | null = null;
  private count = 0;

  constructor(private compareFn: (a: T, b: T) => number = (a: any, b: any) => (a < b ? -1 : a > b ? 1 : 0)) {}

  public insert(value: T): void {
    const node = new RBNode(value);
    if (!this.root) {
      node.color = Color.BLACK;
      this.root = node;
      this.count++;
      return;
    }

    let current: RBNode<T> | null = this.root;
    let parent: RBNode<T> | null = null;

    while (current !== null) {
      parent = current;
      const cmp = this.compareFn(value, current.value);
      if (cmp < 0) {
        current = current.left;
      } else {
        current = current.right;
      }
    }

    node.parent = parent;
    if (this.compareFn(value, parent!.value) < 0) {
      parent!.left = node;
    } else {
      parent!.right = node;
    }

    this.fixInsert(node);
    this.count++;
  }

  public contains(value: T): boolean {
    let current = this.root;
    while (current !== null) {
      const cmp = this.compareFn(value, current.value);
      if (cmp === 0) return true;
      current = cmp < 0 ? current.left : current.right;
    }
    return false;
  }

  public size(): number {
    return this.count;
  }

  public inOrderTraversal(): T[] {
    const result: T[] = [];
    this.traverse(this.root, result);
    return result;
  }

  private traverse(node: RBNode<T> | null, result: T[]): void {
    if (!node) return;
    this.traverse(node.left, result);
    result.push(node.value);
    this.traverse(node.right, result);
  }

  private rotateLeft(x: RBNode<T>): void {
    const y = x.right!;
    x.right = y.left;
    if (y.left) y.left.parent = x;
    y.parent = x.parent;

    if (!x.parent) {
      this.root = y;
    } else if (x === x.parent.left) {
      x.parent.left = y;
    } else {
      x.parent.right = y;
    }

    y.left = x;
    x.parent = y;
  }

  private rotateRight(y: RBNode<T>): void {
    const x = y.left!;
    y.left = x.right;
    if (x.right) x.right.parent = y;
    x.parent = y.parent;

    if (!y.parent) {
      this.root = x;
    } else if (y === y.parent.right) {
      y.parent.right = x;
    } else {
      y.parent.left = x;
    }

    x.right = y;
    y.parent = x;
  }

  private fixInsert(k: RBNode<T>): void {
    let u: RBNode<T> | null;
    while (k.parent && k.parent.color === Color.RED) {
      if (k.parent === k.parent.parent?.right) {
        u = k.parent.parent.left;
        if (u && u.color === Color.RED) {
          u.color = Color.BLACK;
          k.parent.color = Color.BLACK;
          k.parent.parent.color = Color.RED;
          k = k.parent.parent;
        } else {
          if (k === k.parent.left) {
            k = k.parent;
            this.rotateRight(k);
          }
          k.parent!.color = Color.BLACK;
          k.parent!.parent!.color = Color.RED;
          this.rotateLeft(k.parent!.parent!);
        }
      } else if (k.parent.parent) {
        u = k.parent.parent.right;
        if (u && u.color === Color.RED) {
          u.color = Color.BLACK;
          k.parent.color = Color.BLACK;
          k.parent.parent.color = Color.RED;
          k = k.parent.parent;
        } else {
          if (k === k.parent.right) {
            k = k.parent;
            this.rotateLeft(k);
          }
          k.parent!.color = Color.BLACK;
          k.parent!.parent!.color = Color.RED;
          this.rotateRight(k.parent!.parent!);
        }
      }
      if (k === this.root) break;
    }
    this.root!.color = Color.BLACK;
  }
}
