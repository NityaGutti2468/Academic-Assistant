from flask import Blueprint, jsonify
from auth import require_role
from services.marks_service import get_academic_report, notify_marks

marks_bp = Blueprint("marks", __name__)

@marks_bp.route("/marks/<student_id>")
def get_marks(student_id):
    report = get_academic_report(student_id)
    return jsonify(report)


@marks_bp.route("/marks/<student_id>/notify", methods=["POST"])
@require_role("admin")
def send_marks_notification(student_id):
    notification = notify_marks(student_id)
    if not notification:
        return jsonify({"message": "Student not found"}), 404
    return jsonify(notification)
