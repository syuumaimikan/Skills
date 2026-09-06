#!/usr/bin/env python3
"""
Skills Unified CLI - Interactive & Batch Query Tool
Allows running benchmarks, inspecting module telemetry, and triggering automatic commits.
"""

import argparse
import sys
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


def main():
    parser = argparse.ArgumentParser(
        prog="skills-cli",
        description="⚡ Polyglot Skills Core & Findy Optimization CLI"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # Command: status
    subparsers.add_parser("status", help="Display current repository stats and Findy score metrics")

    # Command: bench
    subparsers.add_parser("bench", help="Run multi-language performance benchmarks")

    # Command: commit
    subparsers.add_parser("commit", help="Trigger automated daily commit & metrics sync")

    args = parser.parse_args()

    if args.command == "status":
        latest_json = BASE_DIR / "metrics" / "latest_summary.json"
        if latest_json.exists():
            with open(latest_json, "r", encoding="utf-8") as f:
                data = json.load(f)
            print("=" * 60)
            print(f"📊 Polyglot Engine Status - {data.get('date', 'N/A')}")
            print("=" * 60)
            print(f"Total Lines of Code: {sum(s['lines'] for s in data['codebase_statistics'].values()):,}")
            print("\nLanguage Breakdown:")
            for lang, s in data["codebase_statistics"].items():
                print(f"  • {lang:<12}: {s['files']:>2} files | {s['lines']:>5} lines")
            print("\nKey Performance Indicators:")
            for k, v in data["benchmark_metrics"].items():
                print(f"  • {k:<36}: {v}")
        else:
            print("No metrics generated yet. Run: python scripts/generate_daily_metrics.py")

    elif args.command == "bench":
        import benchmark_runner
        benchmark_runner.run_benchmarks()

    elif args.command == "commit":
        import auto_commit
        auto_commit.main()

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
