#!/usr/bin/env python3
"""Small AppSec automation platform for portfolio demonstration."""

from __future__ import annotations

import html
import re
import sqlite3
from pathlib import Path

from flask import Flask, redirect, request, url_for


BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
DATABASE = BASE_DIR / "appsec.sqlite3"

RULES = [
    ("critical", "Hardcoded secret", re.compile(r"(api[_-]?key|secret|token|password)\s*=\s*['\"][^'\"]{8,}", re.I), "Use a vault or environment variables."),
    ("high", "SQL injection risk", re.compile(r"(SELECT|INSERT|UPDATE|DELETE).*(\+|f\"|f')", re.I), "Use parameterized queries."),
    ("high", "XSS sink", re.compile(r"(innerHTML|document\.write|dangerouslySetInnerHTML)", re.I), "Use safe encoding and sanitization."),
]


def init_db() -> None:
    UPLOAD_DIR.mkdir(exist_ok=True)
    with sqlite3.connect(DATABASE) as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS findings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                severity TEXT NOT NULL,
                title TEXT NOT NULL,
                line INTEGER NOT NULL,
                evidence TEXT NOT NULL,
                remediation TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'open'
            )
        """)


def scan_file(path: Path) -> list[tuple[str, str, int, str, str]]:
    findings = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
        for severity, title, pattern, remediation in RULES:
            if pattern.search(line):
                findings.append((severity, title, line_no, line.strip()[:220], remediation))
    return findings


app = Flask(__name__)


@app.get("/")
def dashboard():
    init_db()
    rows = sqlite3.connect(DATABASE).execute(
        "SELECT severity, COUNT(*) FROM findings GROUP BY severity"
    ).fetchall()
    cards = "".join(f"<div class='metric'><strong>{html.escape(sev)}</strong><span>{count}</span></div>" for sev, count in rows)
    findings = sqlite3.connect(DATABASE).execute(
        "SELECT filename,severity,title,line,status FROM findings ORDER BY id DESC LIMIT 50"
    ).fetchall()
    table = "".join(
        f"<tr><td>{html.escape(f)}</td><td>{html.escape(s)}</td><td>{html.escape(t)}</td><td>{line}</td><td>{html.escape(st)}</td></tr>"
        for f, s, t, line, st in findings
    )
    return f"""<!doctype html><title>AppSec Automation</title><style>
body{{font-family:system-ui;margin:32px;color:#17201d}}.metrics{{display:flex;gap:12px;flex-wrap:wrap}}
.metric{{border:1px solid #dfe5df;border-radius:8px;padding:16px;min-width:140px}}.metric span{{display:block;font-size:2rem}}
td,th{{border:1px solid #dfe5df;padding:8px}}table{{border-collapse:collapse;width:100%;margin-top:20px}}
</style><h1>AppSec Automation Platform</h1>
<form action="/upload" method="post" enctype="multipart/form-data"><input type="file" name="source" required> <button>Upload and scan</button></form>
<h2>Severity dashboard</h2><div class="metrics">{cards or "No findings yet."}</div>
<h2>Latest findings</h2><table><tr><th>File</th><th>Severity</th><th>Title</th><th>Line</th><th>Status</th></tr>{table}</table>"""


@app.post("/upload")
def upload():
    init_db()
    uploaded = request.files["source"]
    safe_name = Path(uploaded.filename or "source.txt").name
    path = UPLOAD_DIR / safe_name
    uploaded.save(path)
    findings = scan_file(path)
    with sqlite3.connect(DATABASE) as db:
        db.executemany(
            "INSERT INTO findings(filename,severity,title,line,evidence,remediation) VALUES(?,?,?,?,?,?)",
            [(safe_name, *finding) for finding in findings],
        )
    if any(f[0] == "critical" for f in findings):
        print("EMAIL ALERT PLACEHOLDER: critical finding detected")
    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    init_db()
    app.run(port=5001, debug=False)
