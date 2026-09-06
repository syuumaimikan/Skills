import crypto from 'node:crypto';

/**
 * High-Performance Merkle Tree Implementation for Cryptographic Verification
 * Used in Blockchain, Git commit hashing, and Distributed File Systems (IPFS).
 */

export class MerkleNode {
  hash: string;
  left: MerkleNode | null;
  right: MerkleNode | null;

  constructor(hash: string, left: MerkleNode | null = null, right: MerkleNode | null = null) {
    this.hash = hash;
    this.left = left;
    this.right = right;
  }
}

export class MerkleTree {
  private root: MerkleNode | null = null;
  private leaves: string[] = [];

  constructor(dataBlocks: string[] = []) {
    if (dataBlocks.length > 0) {
      this.buildTree(dataBlocks);
    }
  }

  private static sha256(data: string): string {
    return crypto.createHash('sha256').update(data).digest('hex');
  }

  public buildTree(dataBlocks: string[]): void {
    if (dataBlocks.length === 0) {
      this.root = null;
      this.leaves = [];
      return;
    }

    this.leaves = dataBlocks.map((d) => MerkleTree.sha256(d));
    let currentLevel: MerkleNode[] = this.leaves.map((h) => new MerkleNode(h));

    while (currentLevel.length > 1) {
      const nextLevel: MerkleNode[] = [];

      for (let i = 0; i < currentLevel.length; i += 2) {
        const left = currentLevel[i];
        if (i + 1 < currentLevel.length) {
          const right = currentLevel[i + 1];
          const combinedHash = MerkleTree.sha256(left.hash + right.hash);
          nextLevel.push(new MerkleNode(combinedHash, left, right));
        } else {
          // Duplicate last odd node if needed
          const combinedHash = MerkleTree.sha256(left.hash + left.hash);
          nextLevel.push(new MerkleNode(combinedHash, left, left));
        }
      }

      currentLevel = nextLevel;
    }

    this.root = currentLevel[0];
  }

  public getRootHash(): string | null {
    return this.root ? this.root.hash : null;
  }

  /**
   * Generates Merkle Audit Proof for verifying inclusion of leaf data.
   */
  public getProof(data: string): { hash: string; position: 'left' | 'right' }[] | null {
    const targetHash = MerkleTree.sha256(data);
    const leafIndex = this.leaves.indexOf(targetHash);
    if (leafIndex === -1) return null;

    const proof: { hash: string; position: 'left' | 'right' }[] = [];
    let currentIndex = leafIndex;
    let currentNodes: string[] = [...this.leaves];

    while (currentNodes.length > 1) {
      const isRightNode = currentIndex % 2 === 1;
      const siblingIndex = isRightNode ? currentIndex - 1 : currentIndex + 1;

      if (siblingIndex < currentNodes.length) {
        proof.push({
          hash: currentNodes[siblingIndex],
          position: isRightNode ? 'left' : 'right',
        });
      } else {
        // Self-paired node
        proof.push({
          hash: currentNodes[currentIndex],
          position: 'right',
        });
      }

      // Compute parent level hashes
      const nextNodes: string[] = [];
      for (let i = 0; i < currentNodes.length; i += 2) {
        if (i + 1 < currentNodes.length) {
          nextNodes.push(MerkleTree.sha256(currentNodes[i] + currentNodes[i + 1]));
        } else {
          nextNodes.push(MerkleTree.sha256(currentNodes[i] + currentNodes[i]));
        }
      }

      currentIndex = Math.floor(currentIndex / 2);
      currentNodes = nextNodes;
    }

    return proof;
  }

  /**
   * Verifies that a given data block is part of the Merkle Tree with the known root hash.
   */
  public static verifyProof(
    data: string,
    proof: { hash: string; position: 'left' | 'right' }[],
    rootHash: string
  ): boolean {
    let currentHash = MerkleTree.sha256(data);

    for (const step of proof) {
      if (step.position === 'left') {
        currentHash = MerkleTree.sha256(step.hash + currentHash);
      } else {
        currentHash = MerkleTree.sha256(currentHash + step.hash);
      }
    }

    return currentHash === rootHash;
  }
}
