from flask import Blueprint
from services.marks_service import get_academic_report, notify_marks

marks_bp = Blueprint("marks", __name__)

@marks_bp.route("/marks/<student_id>")
def get_marks(student_id):

    report = get_academic_report(student_id)

    # Send marks update to parent
    notify_marks(student_id)

    return report