# Docker Security Scanner

Dockerfile security scanner for portfolio container-security checks.

## Features

- Detects missing non-root user.
- Flags broad `COPY .` usage.
- Flags latest tags and exposed privileged ports.
- Produces JSON report.

## Run

```bash
python docker_scan.py --dockerfile Dockerfile --out docker-security-report.json
```

## Keywords

Container Security, Docker, Misconfiguration Checks
