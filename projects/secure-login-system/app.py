#!/usr/bin/env python3
"""Minimal secure login system with JWT and role checks."""

from __future__ import annotations

import datetime as dt
import os
import re
import sqlite3
from functools import wraps
from pathlib import Path

import jwt
from flask import Flask, g, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash


DATABASE = Path(__file__).with_name("users.sqlite3")
JWT_SECRET = os.environ.get("JWT_SECRET", "change-this-secret-before-production")


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["JSON_SORT_KEYS"] = False

    @app.before_request
    def open_database() -> None:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row

    @app.after_request
    def add_security_headers(response):
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "no-referrer"
        return response

    @app.teardown_request
    def close_database(_exception) -> None:
        db = g.pop("db", None)
        if db is not None:
            db.close()

    @app.post("/register")
    def register():
        payload = request.get_json(silent=True) or {}
        username = str(payload.get("username", "")).strip()
        password = str(payload.get("password", ""))
        if not valid_username(username):
            return jsonify(error="Username must be 3-32 characters and use letters, numbers, underscore, or dash."), 400
        if len(password) < 12:
            return jsonify(error="Password must be at least 12 characters."), 400

        try:
            g.db.execute(
                "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                (username, generate_password_hash(password), "user"),
            )
            g.db.commit()
        except sqlite3.IntegrityError:
            return jsonify(error="Username already exists."), 409
        return jsonify(message="Registered successfully."), 201

    @app.post("/login")
    def login():
        payload = request.get_json(silent=True) or {}
        username = str(payload.get("username", "")).strip()
        password = str(payload.get("password", ""))
        user = g.db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        if user is None or not check_password_hash(user["password_hash"], password):
            return jsonify(error="Invalid credentials."), 401
        token = jwt.encode(
            {
                "sub": user["username"],
                "role": user["role"],
                "exp": dt.datetime.now(dt.timezone.utc) + dt.timedelta(minutes=30),
            },
            JWT_SECRET,
            algorithm="HS256",
        )
        return jsonify(access_token=token, token_type="Bearer")

    @app.get("/profile")
    @require_auth()
    def profile():
        return jsonify(username=g.current_user["sub"], role=g.current_user["role"])

    @app.get("/admin")
    @require_auth(role="admin")
    def admin():
        return jsonify(message="Admin route reached.")

    return app


def valid_username(username: str) -> bool:
    return bool(re.fullmatch(r"[A-Za-z0-9_-]{3,32}", username))


def require_auth(role: str | None = None):
    def decorator(view):
        @wraps(view)
        def wrapper(*args, **kwargs):
            auth_header = request.headers.get("Authorization", "")
            scheme, _, token = auth_header.partition(" ")
            if scheme.lower() != "bearer" or not token:
                return jsonify(error="Missing bearer token."), 401
            try:
                claims = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
            except jwt.PyJWTError:
                return jsonify(error="Invalid or expired token."), 401
            if role and claims.get("role") != role:
                return jsonify(error="Insufficient role."), 403
            g.current_user = claims
            return view(*args, **kwargs)
        return wrapper
    return decorator


def init_db() -> None:
    with sqlite3.connect(DATABASE) as db:
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('user', 'admin'))
            )
            """
        )
        db.commit()


app = create_app()


if __name__ == "__main__":
    init_db()
    app.run(debug=False)
