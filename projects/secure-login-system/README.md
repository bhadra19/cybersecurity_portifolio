# Secure Login System with JWT & Input Validation

This project folder contains a minimal secure-login application from the resume and a checklist for expanding it into a full reportable project.

## Target feature set

- Password hashing with Werkzeug or Argon2.
- JWT access tokens with short expiry and role claims.
- Server-side input validation for registration and login.
- SQLite persistence with parameterized queries.
- Role-based access control for user and admin routes.
- Security headers and cookie settings documented in a report.

## Run locally

```bash
pip install -r requirements.txt
python app.py
```

Then register and log in with JSON requests:

```bash
curl -X POST http://127.0.0.1:5000/register -H "Content-Type: application/json" -d "{\"username\":\"arjun\",\"password\":\"change-this-password\"}"
curl -X POST http://127.0.0.1:5000/login -H "Content-Type: application/json" -d "{\"username\":\"arjun\",\"password\":\"change-this-password\"}"
```

## Suggested file structure

```text
app.py
auth.py
database.py
requirements.txt
tests/
  test_auth.py
reports/
  vulnerability-report.md
```

## Vulnerability report sections

1. Scope and test environment.
2. Initial vulnerable behavior.
3. Evidence captured in Burp Suite.
4. Patch implemented.
5. Retest result.
6. Residual risk and hardening notes.

## Resume talking points

- Built secure authentication with JWT and role-based access control.
- Patched SQL injection and broken-auth patterns using parameterized queries and stricter validation.
- Performed self-assessment with Burp Suite and documented the fix cycle.
