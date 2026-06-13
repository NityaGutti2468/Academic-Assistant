from flask import Blueprint, jsonify
from auth import require_mentor_access
from services.mentor_service import get_mentor_students, get_mentor_alerts

mentor_bp = Blueprint("mentor", __name__)

@mentor_bp.route("/mentor/<mentor_id>/students", methods=["GET"])
@require_mentor_access
def route_get_students(mentor_id):
    students = get_mentor_students(mentor_id)
    return jsonify({"students": students})

@mentor_bp.route("/mentor/<mentor_id>/alerts", methods=["GET"])
@require_mentor_access
def route_get_alerts(mentor_id):
    alerts = get_mentor_alerts(mentor_id)
    return jsonify({"alerts": alerts})
