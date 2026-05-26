from database import marks, academic_summary, students
from services.notification_service import send_sms


# ---------- GRADE LOGIC ----------
def calculate_grade(marks):
    if marks >= 90: return "S"
    elif marks >= 80: return "A"
    elif marks >= 70: return "B"
    elif marks >= 60: return "C"
    elif marks >= 50: return "D"
    else: return "F"

def calculate_grade_points(grade):
    points = {"S": 10, "A": 9, "B": 8, "C": 7, "D": 6, "F": 0}
    return points.get(grade, 0)

# ---------- MAIN REPORT ----------
def get_academic_report(student_id):

    student_id = int(student_id)
    student_marks = list(marks.find({"student_id": student_id, "exam_type": "Final"}))

    highest_mark = -1
    lowest_mark = 101
    strongest_subject = None
    weakest_subject = None
    
    total_credits = 0
    total_points = 0
    passed_subjects = 0
    failed_subjects = 0

    for m in student_marks:
        m.pop("_id", None)
        # fallback for missing code
        if "course_code" not in m: m["course_code"] = "UNKNOWN"
            
        m["grade"] = calculate_grade(m["marks"])
        m["grade_points"] = calculate_grade_points(m["grade"])
        m["result"] = "P" if m["grade"] != "F" else "F"
        
        if m["result"] == "P": passed_subjects += 1
        else: failed_subjects += 1
            
        total_credits += m["credits"]
        total_points += (m["grade_points"] * m["credits"])
        
        if m["marks"] > highest_mark:
            highest_mark = m["marks"]
            strongest_subject = m["subject"]
        if m["marks"] < lowest_mark:
            lowest_mark = m["marks"]
            weakest_subject = m["subject"]

    # Calculate exact SGPA / Percentage for the table matching
    real_sgpa = (total_points / total_credits) if total_credits > 0 else 0
    real_percentage = (real_sgpa * 10) - 7.5 if real_sgpa > 0 else 0

    summary = academic_summary.find_one({"student_id": student_id})
    if summary:
        summary.pop("_id", None)
    else:
        summary = {"sgpa": 0, "cgpa": 0, "backlogs": 0}

    # Add real_time computed values for notifications
    summary["real_sgpa"] = round(real_sgpa, 2)
    summary["real_percentage"] = round(real_percentage, 2)
    summary["total_points"] = total_points
    summary["total_credits"] = total_credits
    summary["passed_count"] = passed_subjects
    summary["failed_count"] = failed_subjects

    status = analyze_performance(summary)

    return {
        "marks": student_marks,
        "summary": summary,
        "status": status,
        "insights": {
            "strongest": strongest_subject,
            "weakest": weakest_subject
        }
    }


# ---------- PERFORMANCE ANALYSIS ----------
def analyze_performance(summary):
    sgpa = summary["sgpa"]
    backlogs = summary["backlogs"]
    if backlogs > 2: return "CRITICAL"
    if sgpa < 6: return "WARNING"
    return "GOOD"


# ---------- NOTIFICATION ----------
def notify_marks(student_id):

    student_id = int(student_id)
    report = get_academic_report(student_id)
    student = students.find_one({"student_id": student_id})

    if not student:
        return

    summary = report["summary"]
    marks_list = report["marks"]

    # Build Header as requested
    message = "V Semester\nS.No\tCourse Code\tCourse Name\tNov-25\tGrade\tGrade Points\tCredits\tResult\n"
    
    # Build lines
    idx = 1
    for m in marks_list:
        sub = m.get('subject', 'N/A')
        code = m.get('course_code', 'N/A')
        grd = m.get('grade', 'F')
        pts = m.get('grade_points', 0)
        crd = m.get('credits', 0)
        res = m.get('result', 'F')
        # To match the string exactly: e.g. "1 V23AIT03 DEEP LEARNING S S 10 3.0 P"
        message += f"{idx}\t{code}\t{sub}\t{grd}\t{grd}\t{pts}\t{crd}\t{res}\n"
        idx += 1

    overall_res = "Pass" if summary["failed_count"] == 0 else "Fail"
    pts = summary["total_points"]
    cds = summary["total_credits"]
    sgpa = summary["real_sgpa"]
    perc = summary["real_percentage"]
    
    # Summary Line
    message += f"V Semester Summary Passed:{summary['passed_count']}, Failed:{summary['failed_count']} Result:{overall_res} SGPA:{sgpa:.2f}({pts}/{cds})    {perc:.2f}"

    send_sms(student["parent_phone"], message)