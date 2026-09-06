#!/usr/bin/env python3
"""
Automated Git Commit & Push Bot for Continuous Skill Activity
- Automatically updates daily performance logs
- Generates high-quality conventional commit messages
- Commits and pushes to remote (if git repository is configured)
"""

import subprocess
import sys
import os
import datetime
import random
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = Path(__file__).resolve().parent.parent


def run_cmd(cmd, check=True):
    print(f"👉 Executing: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=BASE_DIR, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"❌ Error (code {result.returncode}):\n{result.stderr}")
    return result


def main():
    print("🚀 Starting Automated Commit Pipeline...")

    # 1. Update daily metrics and benchmark logs
    metrics_script = BASE_DIR / "scripts" / "generate_daily_metrics.py"
    if metrics_script.exists():
        subprocess.run([sys.executable, str(metrics_script)], cwd=BASE_DIR, check=True)

    # 2. Check Git status
    status = run_cmd(["git", "status", "--porcelain"], check=False)
    if status.returncode != 0:
        print("⚠️ Git repository not initialized. Initializing git repo...")
        run_cmd(["git", "init"])
        run_cmd(["git", "branch", "-M", "main"])

    # Stage all changes
    run_cmd(["git", "add", "."])

    # Check if there are staged changes
    diff = run_cmd(["git", "diff", "--cached", "--name-only"], check=False)
    if not diff.stdout.strip():
        # Force a small heartbeat update in METRICS_DIR
        heartbeat_file = BASE_DIR / "metrics" / ".heartbeat"
        heartbeat_file.parent.mkdir(parents=True, exist_ok=True)
        now_str = datetime.datetime.now(datetime.timezone.utc).isoformat()
        with open(heartbeat_file, "w") as f:
            f.write(f"last_activity={now_str}\n")
        run_cmd(["git", "add", str(heartbeat_file)])

    # 3. Create rich conventional commit message
    today_str = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    commit_types = [
        ("perf", "benchmark & algorithmic profiling updates"),
        ("feat", "continuous telemetry and multi-language engine sync"),
        ("refactor", "internal cache pipeline & memory pool alignments"),
        ("chore", "daily repository maintenance & metrics aggregation"),
        ("docs", "technical specification and performance documentation updates"),
    ]
    c_type, c_desc = random.choice(commit_types)
    commit_msg = f"{c_type}(engine): {c_desc} [{today_str}]"

    print(f"📝 Commit message: {commit_msg}")
    commit_res = run_cmd(["git", "commit", "-m", commit_msg], check=False)
    if commit_res.returncode == 0:
        print("✅ Successfully committed changes.")
    else:
        print(f"ℹ️ Git commit output: {commit_res.stdout or commit_res.stderr}")

    # 4. Attempt to push if remote exists
    remotes = run_cmd(["git", "remote"], check=False)
    if remotes.stdout.strip():
        print("🌐 Pushing changes to remote...")
        push_res = run_cmd(["git", "push", "origin", "main"], check=False)
        if push_res.returncode == 0:
            print("🎉 Successfully pushed to GitHub!")
        else:
            print("⚠️ Push failed (check authentication or upstream branch setup).")
    else:
        print("ℹ️ No git remote configured yet. (Run `git remote add origin <url>` when ready)")


if __name__ == "__main__":
    main()
