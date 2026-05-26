from database import attendance, students
from services.notification_service import send_sms

def check_attendance():

    alerts = []

    for r in attendance.find():

        if r["percentage"] < 75:

            student = students.find_one({"student_id": r["student_id"]})

            message = f"""
LOW ATTENDANCE ALERT

Student: {student['name']}
Attendance: {r['percentage']}%

Minimum Required: 75%

Please contact the mentor immediately.
"""

            send_sms(student["parent_phone"], message)

            alerts.append({
                "student_id": r["student_id"],
                "attendance": r["percentage"],
                "status": "LOW ATTENDANCE"
            })

    return alerts

def get_student_attendance(student_id):
    student_id = int(student_id)
    r = attendance.find_one({"student_id": student_id})
    if r:
        r.pop("_id", None)
        return {"message": f"Your attendance is {r['percentage']}%", "data": r}
    return {"message": "Attendance records not found"}