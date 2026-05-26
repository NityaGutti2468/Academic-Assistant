from database import mentors, students, attendance, academic_summary, fees

def add_mentor(data):
    # Data is expected to have: mentor_id, name, department, phone
    mentor_id = int(data.get("mentor_id"))
    
    # Check if mentor exists
    if mentors.find_one({"mentor_id": mentor_id}):
        return {"success": False, "message": "Mentor ID already exists"}
        
    mentors.insert_one(data)
    return {"success": True, "message": "Mentor added successfully"}

def get_all_mentors():
    mentor_list = list(mentors.find({}, {"_id": 0}))
    return mentor_list

def assign_student_mentor(student_id, mentor_id):
    student_id = int(student_id)
    mentor_id = int(mentor_id)
    
    # Check if student exists
    if not students.find_one({"student_id": student_id}):
        return {"success": False, "message": "Student not found"}
        
    students.update_one({"student_id": student_id}, {"$set": {"mentor_id": mentor_id}})
    return {"success": True, "message": f"Student {student_id} assigned to Mentor {mentor_id}"}

def get_all_students_report():
    student_list = list(students.find({}, {"_id": 0}))
    
    report = []
    
    for s in student_list:
        sid = s["student_id"]
        
        # Get attendance
        att = attendance.find_one({"student_id": sid})
        att_perc = att["percentage"] if att else "N/A"
        
        # Get summary
        summary = academic_summary.find_one({"student_id": sid})
        cgpa = summary["cgpa"] if summary else "N/A"
        sgpa = summary["sgpa"] if summary else "N/A"
        
        # Get fees
        fee_records = list(fees.find({"student_id": sid, "status": "pending"}))
        total_due = sum(f["amount"] for f in fee_records)
        fee_status = f"₹{total_due} Pending" if total_due > 0 else "Clear"
        
        report.append({
            "student_id": sid,
            "name": s["name"],
            "mentor_id": s.get("mentor_id", "Unassigned"),
            "attendance": att_perc,
            "sgpa": sgpa,
            "cgpa": cgpa,
            "fees": fee_status
        })
        
    return report
