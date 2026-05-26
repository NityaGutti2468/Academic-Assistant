from flask import Blueprint, request, jsonify
from services.admin_service import add_mentor, get_all_mentors, assign_student_mentor, get_all_students_report
from services.attendance_service import check_attendance
from services.fees_service import check_fees

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/add-mentor", methods=["POST"])
def route_add_mentor():
    data = request.json
    result = add_mentor(data)
    return jsonify(result), 200 if result["success"] else 400

@admin_bp.route("/mentors", methods=["GET"])
def route_get_mentors():
    mentors = get_all_mentors()
    return jsonify({"mentors": mentors})

@admin_bp.route("/assign-mentor", methods=["POST"])
def route_assign_mentor():
    data = request.json
    result = assign_student_mentor(data.get("student_id"), data.get("mentor_id"))
    return jsonify(result), 200 if result["success"] else 400

@admin_bp.route("/students", methods=["GET"])
def route_get_students():
    students = get_all_students_report()
    return jsonify({"students": students})

@admin_bp.route("/trigger-attendance", methods=["POST"])
def route_trigger_attendance():
    alerts = check_attendance()
    return jsonify({"message": "Attendance check completed", "alerts": alerts})

@admin_bp.route("/trigger-fees", methods=["POST"])
def route_trigger_fees():
    alerts = check_fees()
    return jsonify({"message": "Fee check completed", "alerts": alerts})
