#!/usr/bin/env python3
"""Cloud security scanner for local AWS inventory JSON."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def scan_inventory(data: dict) -> list[dict[str, str]]:
    findings = []
    for bucket in data.get("buckets", []):
        if bucket.get("public"):
            findings.append({"severity": "critical", "asset": bucket["name"], "title": "Public S3 bucket", "remediation": "Block public access unless there is an approved business exception."})
        if not bucket.get("encryption"):
            findings.append({"severity": "medium", "asset": bucket["name"], "title": "S3 encryption disabled", "remediation": "Enable default bucket encryption."})
    for policy in data.get("iam_policies", []):
        if "*" in policy.get("actions", []) or "*" in policy.get("resources", []):
            findings.append({"severity": "high", "asset": policy["name"], "title": "Overly broad IAM policy", "remediation": "Replace wildcards with least-privilege actions and resources."})
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Cloud security scanner.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--out", default="cloud-security-report.json")
    args = parser.parse_args()
    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    findings = scan_inventory(data)
    Path(args.out).write_text(json.dumps({"findings": findings}, indent=2), encoding="utf-8")
    print(f"Wrote {args.out} with {len(findings)} findings")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
