# Secure Coding Review Assistant

Rule-based secure code reviewer for Python, JavaScript, and Java snippets.

## Features

- Detects SQL injection patterns.
- Detects reflected XSS sinks.
- Detects hardcoded secrets and tokens.
- Produces severity, evidence, and remediation guidance.

## Run

```bash
python review.py --path ../../projects --out secure-code-findings.json
```

## Keywords

Secure Coding, Application Security, Code Review, Remediation Guidance
