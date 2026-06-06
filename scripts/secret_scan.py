#!/usr/bin/env python3
"""Simple secret detector for CI demonstration."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


SECRET_PATTERN = re.compile(r"(api[_-]?key|secret|token|password)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{12,}", re.I)


def main() -> int:
    parser = argparse.ArgumentParser(description="Secret detection scanner.")
    parser.add_argument("--path", required=True)
    parser.add_argument("--out", default="secret-findings.json")
    args = parser.parse_args()
    root = Path(args.path)
    findings = []
    for file in root.rglob("*"):
        if not file.is_file() or ".git" in file.parts:
            continue
        if file.suffix.lower() not in {".py", ".js", ".java", ".yml", ".yaml", ".json", ".env", ".txt"}:
            continue
        for line_no, line in enumerate(file.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
            if SECRET_PATTERN.search(line):
                findings.append({"file": str(file), "line": line_no, "severity": "critical", "title": "Possible secret"})
    Path(args.out).write_text(json.dumps({"findings": findings}, indent=2), encoding="utf-8")
    print(f"Wrote {args.out} with {len(findings)} findings")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
