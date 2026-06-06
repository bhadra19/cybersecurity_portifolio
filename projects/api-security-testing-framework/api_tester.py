#!/usr/bin/env python3
"""Authorized API security testing framework."""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request


def request(url: str, token: str | None = None) -> tuple[int, str]:
    headers = {"User-Agent": "PortfolioApiSecurityTester/1.0"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=5) as response:
            return response.status, response.read(1000).decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read(1000).decode("utf-8", errors="replace")
    except OSError as exc:
        return 0, str(exc)


def main() -> int:
    parser = argparse.ArgumentParser(description="Authorized API security tester.")
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--token")
    parser.add_argument("--i-own-this-target", action="store_true")
    parser.add_argument("--out", default="api-security-report.json")
    args = parser.parse_args()
    if not args.i_own_this_target:
        print("Refusing to test without --i-own-this-target.", file=sys.stderr)
        return 2
    base = args.base_url.rstrip("/")
    checks = []
    for path in ["/api/profile", "/api/users/1", "/api/users/2"]:
        status, body = request(base + path)
        checks.append({"check": "missing_jwt", "path": path, "status": status, "risk": "high" if status == 200 else "info"})
        if args.token:
            status, body = request(base + path, args.token)
            checks.append({"check": "authorized_request", "path": path, "status": status, "sample": body[:120]})
    start = time.time()
    statuses = [request(base + "/api/profile", args.token)[0] for _ in range(10)]
    checks.append({"check": "rate_limit_observation", "requests": 10, "seconds": round(time.time() - start, 2), "statuses": statuses})
    fuzz_url = base + "/api/search?q=" + urllib.parse.quote("'\"<script>alert(1)</script>")
    status, body = request(fuzz_url, args.token)
    checks.append({"check": "api_fuzzing", "path": "/api/search", "status": status, "reflected_payload": "<script>" in body})
    with open(args.out, "w", encoding="utf-8") as handle:
        json.dump({"base_url": base, "checks": checks}, handle, indent=2)
    print(f"Wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
