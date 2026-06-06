#!/usr/bin/env python3
"""Dependency review scanner for portfolio CI."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


RISKY_PINS = {"Flask==0.12": "Known old Flask release", "PyJWT==1.7.0": "Old JWT library release"}


def main() -> int:
    parser = argparse.ArgumentParser(description="Dependency review scanner.")
    parser.add_argument("--path", required=True)
    parser.add_argument("--out", default="dependency-findings.json")
    args = parser.parse_args()
    findings = []
    for file in Path(args.path).rglob("requirements.txt"):
        for line_no, line in enumerate(file.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
            clean = line.strip()
            if clean in RISKY_PINS:
                findings.append({"file": str(file), "line": line_no, "severity": "high", "title": RISKY_PINS[clean]})
            elif clean and "==" not in clean:
                findings.append({"file": str(file), "line": line_no, "severity": "low", "title": "Dependency is not version pinned"})
    Path(args.out).write_text(json.dumps({"findings": findings}, indent=2), encoding="utf-8")
    print(f"Wrote {args.out} with {len(findings)} findings")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
