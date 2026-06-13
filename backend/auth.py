import os
from functools import wraps

from flask import Blueprint, jsonify, request, session


auth_bp = Blueprint("auth", __name__)


def _unauthorized():
    return jsonify({"message": "Authentication required"}), 401


def require_role(role):
    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            if session.get("role") != role:
                return _unauthorized()
            return view(*args, **kwargs)

        return wrapped

    return decorator


def require_mentor_access(view):
    @wraps(view)
    def wrapped(mentor_id, *args, **kwargs):
        role = session.get("role")
        if role == "admin":
            return view(mentor_id, *args, **kwargs)
        if role != "mentor" or str(session.get("user_id")) != str(mentor_id):
            return _unauthorized()
        return view(mentor_id, *args, **kwargs)

    return wrapped


@auth_bp.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    user_id = str(data.get("user_id", "")).strip()
    password = str(data.get("password", ""))

    admin_password = os.getenv("DASHBOARD_ADMIN_PASSWORD")
    mentor_password = os.getenv("DASHBOARD_MENTOR_PASSWORD")

    if user_id == "admin" and admin_password and password == admin_password:
        session.clear()
        session.update({"role": "admin", "user_id": "admin"})
        return jsonify({"role": "Admin", "user_id": "admin"})

    if user_id.isdigit() and mentor_password and password == mentor_password:
        session.clear()
        session.update({"role": "mentor", "user_id": user_id})
        return jsonify({"role": "Mentor", "user_id": user_id})

    return jsonify({"message": "Invalid credentials"}), 401


@auth_bp.route("/auth/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message": "Logged out"})


@auth_bp.route("/auth/session")
def current_session():
    role = session.get("role")
    if not role:
        return _unauthorized()
    return jsonify({"role": role.title(), "user_id": session.get("user_id")})
