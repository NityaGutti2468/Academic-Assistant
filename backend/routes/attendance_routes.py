from flask import Blueprint
from services.attendance_service import check_attendance

attendance_bp = Blueprint("attendance", __name__)

@attendance_bp.route("/check-attendance")

def attendance_alert():

    alerts = check_attendance()

    return {"alerts": alerts}