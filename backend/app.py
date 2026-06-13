from pathlib import Path
import secrets

from flask import Flask, redirect, send_from_directory
from flask_cors import CORS
import os

from auth import auth_bp
from routes.attendance_routes import attendance_bp
from routes.marks_routes import marks_bp
from routes.fees_routes import fees_bp
from routes.voice_routes import voice_bp
from routes.admin_routes import admin_bp
from routes.mentor_routes import mentor_bp
from routes.dashboard_routes import dashboard_bp

from services.attendance_service import check_attendance
from services.fees_service import check_fees

FRONTEND_DIR = Path(__file__).resolve().parents[1] / "frontend"

app = Flask(__name__)
app.config.update(
    SECRET_KEY=os.getenv("SECRET_KEY") or secrets.token_hex(32),
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=os.getenv("VERCEL") == "1",
)
CORS(app)

app.register_blueprint(auth_bp)
app.register_blueprint(attendance_bp)
app.register_blueprint(marks_bp)
app.register_blueprint(fees_bp)
app.register_blueprint(voice_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(mentor_bp)
app.register_blueprint(dashboard_bp)


@app.route("/")
def home():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.route("/mentor")
def mentor_dashboard():
    return redirect("/dashboard")


@app.route("/frontend/<path:filename>")
def frontend_asset(filename):
    return send_from_directory(FRONTEND_DIR, filename)


@app.route("/api/health")
def health():
    return {"status": "ok", "message": "Multi-Agent Academic System Running"}


# -------- AGENTS --------

def monitor_attendance():
    print("Running attendance agent...")
    check_attendance()


def monitor_fees():
    print("Running fee monitoring agent...")
    check_fees()


# -------- SCHEDULER --------


def start_scheduler():
    if os.getenv("ENABLE_SCHEDULER", "false").lower() != "true":
        print("Scheduler disabled. Set ENABLE_SCHEDULER=true to enable background agents.")
        return

    from apscheduler.schedulers.background import BackgroundScheduler

    scheduler = BackgroundScheduler()
    scheduler.add_job(monitor_attendance, "interval", minutes=10)
    scheduler.add_job(monitor_fees, "interval", minutes=30)
    scheduler.start()
    print("Scheduler started.")


start_scheduler()


if __name__ == "__main__":
    app.run(debug=True)
