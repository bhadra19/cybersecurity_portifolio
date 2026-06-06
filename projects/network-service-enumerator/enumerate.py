#!/usr/bin/env python3
"""Consent-gated TCP service enumerator for lab hosts."""

from __future__ import annotations

import argparse
import csv
import socket
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path


def parse_ports(raw: str) -> list[int]:
    ports: set[int] = set()
    for part in raw.split(","):
        part = part.strip()
        if "-" in part:
            start, end = [int(value) for value in part.split("-", 1)]
            ports.update(range(start, end + 1))
        elif part:
            ports.add(int(part))
    return sorted(port for port in ports if 1 <= port <= 65535)


def scan_port(host: str, port: int, timeout: float) -> dict[str, str | int]:
    result: dict[str, str | int] = {"host": host, "port": port, "state": "closed", "banner": ""}
    try:
        with socket.create_connection((host, port), timeout=timeout) as sock:
            result["state"] = "open"
            sock.settimeout(timeout)
            try:
                sock.sendall(b"\r\n")
                banner = sock.recv(160).decode("utf-8", errors="replace").strip()
                result["banner"] = banner
            except OSError:
                result["banner"] = ""
    except OSError:
        pass
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Authorized-use TCP service enumerator.")
    parser.add_argument("--host", required=True, help="Single host you are authorized to scan.")
    parser.add_argument("--ports", default="1-1024", help="Comma-separated ports or ranges, for example 22,80,443,8000-8010.")
    parser.add_argument("--timeout", type=float, default=1.5)
    parser.add_argument("--workers", type=int, default=64)
    parser.add_argument("--out", default="service-results.csv")
    parser.add_argument("--i-own-this-target", action="store_true", help="Required consent confirmation.")
    args = parser.parse_args()

    if not args.i_own_this_target:
        print("Refusing to scan without --i-own-this-target consent confirmation.", file=sys.stderr)
        return 2

    ports = parse_ports(args.ports)
    if not ports:
        print("No valid ports were provided.", file=sys.stderr)
        return 2

    rows = []
    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as executor:
        futures = [executor.submit(scan_port, args.host, port, args.timeout) for port in ports]
        for future in as_completed(futures):
            row = future.result()
            if row["state"] == "open":
                rows.append(row)
                print(f"{row['host']}:{row['port']} open {row['banner']}")

    out_path = Path(args.out)
    with out_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["host", "port", "state", "banner"])
        writer.writeheader()
        writer.writerows(sorted(rows, key=lambda item: int(item["port"])))
    print(f"Wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
