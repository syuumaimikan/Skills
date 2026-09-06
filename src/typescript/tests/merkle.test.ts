import { test, describe } from 'node:test';
import assert from 'node:assert';
import { MerkleTree } from '../data_structures/merkle_tree.js';

describe('Merkle Tree Cryptographic Verification', () => {
  test('Root hash calculation and tree consistency', () => {
    const data = ['block_0', 'block_1', 'block_2', 'block_3'];
    const tree = new MerkleTree(data);

    const root = tree.getRootHash();
    assert.ok(root);
    assert.strictEqual(typeof root, 'string');
    assert.strictEqual(root.length, 64); // SHA-256 hex string
  });

  test('Audit Proof Generation and Verification', () => {
    const data = ['tx_alice_bob', 'tx_bob_charlie', 'tx_charlie_dave', 'tx_dave_eve'];
    const tree = new MerkleTree(data);
    const rootHash = tree.getRootHash()!;

    const target = 'tx_bob_charlie';
    const proof = tree.getProof(target);
    assert.ok(proof);

    const isValid = MerkleTree.verifyProof(target, proof, rootHash);
    assert.strictEqual(isValid, true);

    const isInvalid = MerkleTree.verifyProof('tampered_transaction', proof, rootHash);
    assert.strictEqual(isInvalid, false);
  });
});
