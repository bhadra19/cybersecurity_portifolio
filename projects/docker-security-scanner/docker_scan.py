#!/usr/bin/env python3
"""Dockerfile security scanner."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def scan(dockerfile: Path) -> list[dict[str, str]]:
    text = dockerfile.read_text(encoding="utf-8", errors="replace")
    findings = []
    if re.search(r"^FROM\s+\S+:latest\b", text, re.I | re.M):
        findings.append({"severity": "medium", "title": "Base image uses latest tag", "remediation": "Pin base images to explicit versions or digests."})
    if not re.search(r"^USER\s+(?!root\b)\S+", text, re.I | re.M):
        findings.append({"severity": "high", "title": "Container may run as root", "remediation": "Create and switch to a non-root user."})
    if re.search(r"^COPY\s+\.\s+", text, re.I | re.M):
        findings.append({"severity": "medium", "title": "Broad COPY directive", "remediation": "Copy only required files and use .dockerignore."})
    if re.search(r"^EXPOSE\s+(22|2375|2376)\b", text, re.I | re.M):
        findings.append({"severity": "high", "title": "Sensitive port exposed", "remediation": "Avoid exposing SSH or Docker daemon ports in application containers."})
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Dockerfile security scanner.")
    parser.add_argument("--dockerfile", required=True)
    parser.add_argument("--out", default="docker-security-report.json")
    args = parser.parse_args()
    findings = scan(Path(args.dockerfile))
    Path(args.out).write_text(json.dumps({"findings": findings}, indent=2), encoding="utf-8")
    print(f"Wrote {args.out} with {len(findings)} findings")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
