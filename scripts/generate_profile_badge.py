#!/usr/bin/env python3
"""
Generates animated SVG skill matrix badges suitable for embedding in GitHub Profile READMEs.
"""

import sys
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
METRICS_DIR = BASE_DIR / "metrics"

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


def generate_skill_matrix_svg():
    METRICS_DIR.mkdir(parents=True, exist_ok=True)
    summary_file = METRICS_DIR / "latest_summary.json"
    
    if summary_file.exists():
        with open(summary_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            stats = data.get("codebase_statistics", {})
    else:
        stats = {
            "TypeScript": {"lines": 737},
            "Python": {"lines": 718},
            "Rust": {"lines": 480},
            "Go": {"lines": 319},
            "C++": {"lines": 182},
            "Kotlin": {"lines": 119},
            "C#": {"lines": 65},
        }

    total_lines = sum(s.get("lines", 0) for s in stats.values()) or 1

    lang_colors = {
        "TypeScript": "#3178c6",
        "Python": "#3572A5",
        "Rust": "#dea584",
        "Go": "#00ADD8",
        "C++": "#f34b7d",
        "Kotlin": "#A97BFF",
        "C#": "#178600",
    }

    # Build SVG progress bars
    rows_svg = ""
    y_offset = 65
    for lang, info in stats.items():
        lines = info.get("lines", 0)
        pct = (lines / total_lines) * 100
        color = lang_colors.get(lang, "#6366f1")
        bar_width = int((lines / total_lines) * 320)

        rows_svg += f"""
    <g transform="translate(30, {y_offset})">
      <text x="0" y="12" fill="#e2e8f0" font-family="-apple-system,BlinkMacSystemFont,sans-serif" font-size="13" font-weight="600">{lang}</text>
      <rect x="110" y="0" width="320" height="14" rx="7" fill="rgba(255,255,255,0.06)"/>
      <rect x="110" y="0" width="{bar_width}" height="14" rx="7" fill="{color}"/>
      <text x="445" y="12" fill="#94a3b8" font-family="-apple-system,BlinkMacSystemFont,sans-serif" font-size="12">{lines:,} lines ({pct:.1f}%)</text>
    </g>"""
        y_offset += 28

    svg_height = y_offset + 30
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="600" height="{svg_height}" viewBox="0 0 600 {svg_height}">
  <defs>
    <linearGradient id="card-bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0b0f19" />
      <stop offset="100%" stop-color="#171e2e" />
    </linearGradient>
  </defs>
  <rect width="100%" height="100%" rx="16" fill="url(#card-bg)" stroke="rgba(255,255,255,0.08)" stroke-width="1.5"/>
  <text x="30" y="38" fill="#f8fafc" font-family="-apple-system,BlinkMacSystemFont,sans-serif" font-size="18" font-weight="bold">⚡ Polyglot Multi-Language Distribution</text>
  <text x="570" y="38" fill="#38bdf8" font-family="-apple-system,BlinkMacSystemFont,sans-serif" font-size="13" font-weight="600" text-anchor="end">Total: {total_lines:,} LOC</text>
  {rows_svg}
</svg>"""

    output_path = METRICS_DIR / "language_matrix.svg"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg)

    print(f"✅ Generated language matrix SVG at {output_path}")


if __name__ == "__main__":
    generate_skill_matrix_svg()
