from database import students, attendance, academic_summary, fees, alert_logs
from services.attendance_service import check_attendance

def get_mentor_students(mentor_id):
    mentor_id = str(mentor_id) # Ensure format consistency or maintain int
    try:
        mentor_id = int(mentor_id)
    except:
        pass

    assigned_students = list(students.find({"mentor_id": mentor_id}, {"_id": 0}))
    
    report = []
    
    for s in assigned_students:
        sid = s["student_id"]
        
        # Get attendance
        att = attendance.find_one({"student_id": sid})
        att_perc = att["percentage"] if att else "N/A"
        
        # Get summary
        summary = academic_summary.find_one({"student_id": sid})
        cgpa = summary["cgpa"] if summary else "N/A"
        sgpa = summary["sgpa"] if summary else "N/A"
        backlogs = summary["backlogs"] if summary else 0
        
        # Get fees
        fee_records = list(fees.find({"student_id": sid, "status": "pending"}))
        total_due = sum(f["amount"] for f in fee_records)
        fee_status = f"₹{total_due} Pending" if total_due > 0 else "Clear"
        
        report.append({
            "student_id": sid,
            "name": s["name"],
            "attendance": att_perc,
            "sgpa": sgpa,
            "cgpa": cgpa,
            "backlogs": backlogs,
            "fees": fee_status
        })
        
    return report

def get_mentor_alerts(mentor_id):
    # Fetch students for this mentor
    mentor_id = int(mentor_id)
    assigned_students = list(students.find({"mentor_id": mentor_id}, {"_id": 0}))
    assigned_ids = [s["student_id"] for s in assigned_students]
    
    alerts = []
    
    # 1. Attendance Alerts
    for sid in assigned_ids:
        att = attendance.find_one({"student_id": sid})
        if att and att["percentage"] < 75:
            alerts.append({
                "student_id": sid,
                "type": "Low Attendance",
                "message": f"Attendance is {att['percentage']}%",
                "severity": "High"
            })
            
    # 2. Academic Alerts
    for sid in assigned_ids:
        summary = academic_summary.find_one({"student_id": sid})
        if summary and (summary["cgpa"] < 6 or summary["backlogs"] >= 2):
            alerts.append({
                "student_id": sid,
                "type": "Academic Warning",
                "message": f"CGPA: {summary['cgpa']}, Backlogs: {summary['backlogs']}",
                "severity": "High" if summary["backlogs"] >= 3 else "Medium"
            })
            
    # 3. Fee Alerts
    for sid in assigned_ids:
        fee_records = list(fees.find({"student_id": sid, "status": "pending"}))
        if fee_records:
            total = sum(f["amount"] for f in fee_records)
            alerts.append({
                "student_id": sid,
                "type": "Fee Pending",
                "message": f"₹{total} is owed across {len(fee_records)} record(s)",
                "severity": "Medium"
            })
            
    return alerts
