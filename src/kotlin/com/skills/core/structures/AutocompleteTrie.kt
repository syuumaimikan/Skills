package com.skills.core.structures

import java.util.concurrent.ConcurrentHashMap

/**
 * High-Performance Prefix Trie with Word Frequency & Autocomplete
 * Thread-safe and optimized for ultra-fast prefix searches.
 */
class TrieNode(
    val children: ConcurrentHashMap<Char, TrieNode> = ConcurrentHashMap(),
    var isEndOfWord: Boolean = false,
    var frequency: Int = 0
)

class AutocompleteTrie {
    private val root = TrieNode()

    /**
     * Inserts a word into the Trie with an initial frequency or increments existing.
     */
    fun insert(word: String, frequency: Int = 1) {
        var current = root
        for (ch in word) {
            current = current.children.computeIfAbsent(ch) { TrieNode() }
        }
        current.isEndOfWord = true
        current.frequency += frequency
    }

    /**
     * Searches for exact word match and returns its frequency, or 0 if not found.
     */
    fun search(word: String): Int {
        var current = root
        for (ch in word) {
            current = current.children[ch] ?: return 0
        }
        return if (current.isEndOfWord) current.frequency else 0
    }

    /**
     * Checks if any word starts with the given prefix.
     */
    fun startsWith(prefix: String): Boolean {
        var current = root
        for (ch in prefix) {
            current = current.children[ch] ?: return false
        }
        return true
    }

    /**
     * Autocomplete suggestion: Returns top K words matching the prefix ordered by frequency.
     */
    fun autocomplete(prefix: String, topK: Int = 5): List<Pair<String, Int>> {
        var current = root
        for (ch in prefix) {
            current = current.children[ch] ?: return emptyList()
        }

        val results = mutableListOf<Pair<String, Int>>()
        dfsCollect(current, StringBuilder(prefix), results)

        return results.sortedByDescending { it.second }.take(topK)
    }

    private fun dfsCollect(node: TrieNode, currentWord: StringBuilder, results: MutableList<Pair<String, Int>>) {
        if (node.isEndOfWord) {
            results.add(currentWord.toString() to node.frequency)
        }

        for ((ch, childNode) in node.children) {
            currentWord.append(ch)
            dfsCollect(childNode, currentWord, results)
            currentWord.deleteCharAt(currentWord.length - 1)
        }
    }
}
