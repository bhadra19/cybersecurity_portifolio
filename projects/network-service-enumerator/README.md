# Network Port Scanner & Service Enumerator

Portfolio implementation for a consent-gated TCP scanner and banner collector.

## What it does

- Scans selected TCP ports on a single authorized host.
- Uses concurrent socket connections for speed.
- Attempts safe banner collection for open services.
- Writes CSV output for reporting.

## Authorized-use boundary

Run this only on hosts you own or have permission to test. The script requires an explicit `--i-own-this-target` flag before it will run.

## Example

```bash
python enumerate.py --host 127.0.0.1 --ports 22,80,443,5000 --i-own-this-target --out results.csv
```
