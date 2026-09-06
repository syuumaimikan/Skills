# 🤝 Contributing to Polyglot Skills Core

Thank you for your interest in contributing! This project is an open-source high-performance algorithms and polyglot systems foundation.

---

## 🛠️ Development Setup

### 1. Prerequisites
- **Node.js**: v20+
- **Python**: 3.10+
- **Rust**: 1.75+ (Cargo)
- **Go**: 1.21+
- **C++**: Clang / GCC with C++20 support

### 2. Running Local Tests
```bash
# TypeScript
npm install
npm test

# Python
python -m unittest discover -s src/python/tests -p "test_*.py"

# Rust
cargo test

# Go
go test ./...
```

---

## 📝 Commit Convention

We adhere strictly to [Conventional Commits](https://www.conventionalcommits.org/):

- `feat(scope)`: New feature or algorithm module
- `fix(scope)`: Bug fix
- `perf(scope)`: Performance optimization or SIMD tuning
- `docs(scope)`: Documentation, architecture specs, or benchmarks
- `chore(scope)`: CI/CD, build tools, or metrics automation

---

## 🚀 Pull Request Process

1. Fork the repository and create your branch from `main`.
2. Ensure all multi-language tests pass locally (`npm test`, `pytest`, `cargo test`, `go test`).
3. Include benchmarks or complexity analysis if introducing new data structures.
4. Open a Pull Request using our [PR Template](.github/PULL_REQUEST_TEMPLATE.md).
