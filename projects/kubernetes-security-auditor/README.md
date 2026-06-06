# Kubernetes Security Auditor

Kubernetes manifest auditor for RBAC and pod security checks.

## Features

- Flags privileged containers.
- Flags hostPath usage.
- Flags missing CPU/memory limits.
- Flags broad RBAC wildcard permissions.

## Run

```bash
python kube_audit.py --path manifests --out kube-audit-report.json
```

## Keywords

Kubernetes, Cloud Security, RBAC, Pod Security
