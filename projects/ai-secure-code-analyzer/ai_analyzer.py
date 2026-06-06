#!/usr/bin/env python3
"""AI-style secure code analyzer with deterministic rules."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


RULES = [
    {
        "title": "SQL injection risk",
        "severity": "high",
        "pattern": re.compile(r"SELECT .*(\+|f\"|f')", re.I),
        "explanation": "The query appears to combine SQL text with user-controlled input. Attackers can alter query structure.",
        "fix": "Use parameterized queries, for example db.execute('SELECT * FROM users WHERE username = ?', (username,)).",
    },
    {
        "title": "XSS risk",
        "severity": "high",
        "pattern": re.compile(r"return\s+[\"']<.*\+", re.I),
        "explanation": "HTML is being assembled with untrusted data. This can allow script injection in a browser.",
        "fix": "Escape output through a trusted template engine or encode user content before rendering.",
    },
]


def analyze(path: Path) -> list[dict[str, object]]:
    findings = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
        for rule in RULES:
            if rule["pattern"].search(line):
                findings.append({
                    "file": str(path),
                    "line": line_no,
                    "severity": rule["severity"],
                    "title": rule["title"],
                    "evidence": line.strip(),
                    "explanation": rule["explanation"],
                    "remediation": rule["fix"],
                })
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="AI-powered secure code analyzer.")
    parser.add_argument("--file", required=True)
    parser.add_argument("--out", default="ai-code-report.json")
    args = parser.parse_args()
    findings = analyze(Path(args.file))
    Path(args.out).write_text(json.dumps({"findings": findings}, indent=2), encoding="utf-8")
    print(f"Wrote {args.out} with {len(findings)} findings")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
