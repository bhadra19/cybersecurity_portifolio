#!/usr/bin/env python3
"""Lightweight Kubernetes manifest security auditor."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


CHECKS = [
    ("critical", "Privileged container", re.compile(r"privileged:\s*true", re.I), "Disable privileged mode."),
    ("high", "hostPath volume", re.compile(r"hostPath:", re.I), "Avoid hostPath or restrict to read-only approved paths."),
    ("medium", "Wildcard RBAC permission", re.compile(r"resources:\s*\n\s*-\s*['\"]?\*|verbs:\s*\n\s*-\s*['\"]?\*", re.I), "Use least-privilege RBAC."),
]


def audit_file(path: Path) -> list[dict[str, object]]:
    text = path.read_text(encoding="utf-8", errors="replace")
    findings = []
    for severity, title, pattern, remediation in CHECKS:
        if pattern.search(text):
            findings.append({"file": str(path), "severity": severity, "title": title, "remediation": remediation})
    if "kind: Pod" in text or "kind: Deployment" in text:
        if "limits:" not in text:
            findings.append({"file": str(path), "severity": "medium", "title": "Missing resource limits", "remediation": "Set CPU and memory limits."})
        if "runAsNonRoot: true" not in text:
            findings.append({"file": str(path), "severity": "medium", "title": "runAsNonRoot not enforced", "remediation": "Set securityContext.runAsNonRoot to true."})
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Kubernetes security auditor.")
    parser.add_argument("--path", required=True)
    parser.add_argument("--out", default="kube-audit-report.json")
    args = parser.parse_args()
    root = Path(args.path)
    files = [root] if root.is_file() else list(root.rglob("*.yml")) + list(root.rglob("*.yaml"))
    findings = [finding for file in files for finding in audit_file(file)]
    Path(args.out).write_text(json.dumps({"findings": findings}, indent=2), encoding="utf-8")
    print(f"Wrote {args.out} with {len(findings)} findings")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
