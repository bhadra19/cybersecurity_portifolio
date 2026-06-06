#!/usr/bin/env python3
"""Rule-based secure coding review assistant."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


RULES = [
    {
        "id": "SQLI-001",
        "severity": "high",
        "pattern": re.compile(r"(SELECT|INSERT|UPDATE|DELETE).*(\+|f\"|f')", re.IGNORECASE),
        "title": "Possible SQL injection through string-built query",
        "remediation": "Use parameterized queries or an ORM query builder.",
    },
    {
        "id": "XSS-001",
        "severity": "high",
        "pattern": re.compile(r"(innerHTML|document\.write|dangerouslySetInnerHTML)", re.IGNORECASE),
        "title": "Possible XSS sink",
        "remediation": "Prefer safe templating, output encoding, and strict sanitization.",
    },
    {
        "id": "SECRET-001",
        "severity": "critical",
        "pattern": re.compile(r"(api[_-]?key|secret|token|password)\s*=\s*['\"][^'\"]{8,}", re.IGNORECASE),
        "title": "Possible hardcoded secret",
        "remediation": "Move secrets to a vault or environment variables and rotate exposed values.",
    },
]


def review_file(path: Path) -> list[dict[str, object]]:
    findings: list[dict[str, object]] = []
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return findings
    for number, line in enumerate(lines, start=1):
        for rule in RULES:
            if rule["pattern"].search(line):
                findings.append({
                    "rule": rule["id"],
                    "severity": rule["severity"],
                    "title": rule["title"],
                    "file": str(path),
                    "line": number,
                    "evidence": line.strip()[:220],
                    "remediation": rule["remediation"],
                })
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Secure coding review assistant.")
    parser.add_argument("--path", required=True, help="File or directory to review.")
    parser.add_argument("--out", default="secure-code-findings.json")
    args = parser.parse_args()
    root = Path(args.path)
    files = [root] if root.is_file() else [
        p for p in root.rglob("*")
        if p.suffix.lower() in {".py", ".js", ".jsx", ".ts", ".tsx", ".java"}
    ]
    findings = [finding for file in files for finding in review_file(file)]
    Path(args.out).write_text(json.dumps({"findings": findings}, indent=2), encoding="utf-8")
    print(f"Wrote {args.out} with {len(findings)} findings")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
