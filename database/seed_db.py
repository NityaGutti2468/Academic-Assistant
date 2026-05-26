from pymongo import MongoClient
from datetime import datetime, timedelta
import random

client = MongoClient("mongodb://localhost:27017")
db = client["college_ai"]

def seed_database():
    # Clear existing data
    db.students.delete_many({})
    db.attendance.delete_many({})
    db.marks.delete_many({})
    db.academic_summary.delete_many({})
    db.fees.delete_many({})
    db.alert_logs.delete_many({})
    db.mentors.delete_many({})

    # 1. Add Mentors
    mentors = [
         {"mentor_id": 101, "name": "Dr. Rao", "department": "Computer Science", "phone": "+919876543211", "email": "rao@college.edu"},
         {"mentor_id": 102, "name": "Prof. Smith", "department": "Electronics", "phone": "+919876543212", "email": "smith@college.edu"}
    ]
    db.mentors.insert_many(mentors)

    # 2. Add Students
    students = [
        {"student_id": 1, "name": "Alex Johnson", "department": "Computer Science", "parent_phone": "+919876543210", "mentor_id": 101},
        {"student_id": 2, "name": "Maria Garcia", "department": "Computer Science", "parent_phone": "+919876543213", "mentor_id": 101},
        {"student_id": 3, "name": "David Chen", "department": "Electronics", "parent_phone": "+919876543214", "mentor_id": 102}
    ]
    db.students.insert_many(students)

    # 3. Add Attendance
    attendance = [
        {"student_id": 1, "total_classes": 100, "attended_classes": 70, "percentage": 70.0}, # Alert
        {"student_id": 2, "total_classes": 100, "attended_classes": 95, "percentage": 95.0}, # Safe
        {"student_id": 3, "total_classes": 100, "attended_classes": 60, "percentage": 60.0}  # Alert
    ]
    db.attendance.insert_many(attendance)

    # 4. Add Marks (focusing on 'Final' exams for insight profiler)
    marks_data = [
        # Alex (Student 1) -> V Semester
        {"student_id": 1, "course_code": "V23AIT04", "subject": "COMPUTER NETWORKS", "marks": 85, "credits": 3.0, "exam_type": "Final"},
        {"student_id": 1, "course_code": "V23AIT03", "subject": "DEEP LEARNING", "marks": 92, "credits": 3.0, "exam_type": "Final"},
        {"student_id": 1, "course_code": "V23MLT01", "subject": "NATURAL LANGUAGE PROCESSING", "marks": 88, "credits": 3.0, "exam_type": "Final"},
        {"student_id": 1, "course_code": "V23CSSE03", "subject": "FULL STACK DEVELOPMENT-II", "marks": 96, "credits": 2.0, "exam_type": "Final"},
        
        # Maria (Student 2)
        {"student_id": 2, "course_code": "V23AIT04", "subject": "COMPUTER NETWORKS", "marks": 90, "credits": 3.0, "exam_type": "Final"},
        {"student_id": 2, "course_code": "V23AIT03", "subject": "DEEP LEARNING", "marks": 80, "credits": 3.0, "exam_type": "Final"},
        {"student_id": 2, "course_code": "V23CSSE03", "subject": "FULL STACK DEVELOPMENT-II", "marks": 95, "credits": 2.0, "exam_type": "Final"},
        
        # David (Student 3) -> Struggling badly
        {"student_id": 3, "course_code": "V23AIT04", "subject": "COMPUTER NETWORKS", "marks": 35, "credits": 3.0, "exam_type": "Final"},
        {"student_id": 3, "course_code": "V23AIT03", "subject": "DEEP LEARNING", "marks": 40, "credits": 3.0, "exam_type": "Final"}
    ]
    db.marks.insert_many(marks_data)

    # 5. Add Academic Summary
    summary_data = [
        {"student_id": 1, "cgpa": 7.5, "sgpa": 7.2, "backlogs": 0},
        {"student_id": 2, "cgpa": 8.8, "sgpa": 9.0, "backlogs": 0},
        {"student_id": 3, "cgpa": 5.2, "sgpa": 4.8, "backlogs": 2} # Critical Alert
    ]
    db.academic_summary.insert_many(summary_data)

    # 6. Add Fees
    today = datetime.now()
    fees_data = [
        # Student 1: 1 upcoming, 1 overdue by 10 days to show severe penalty (₹500 penalty)
        {"student_id": 1, "fee_type": "Tuition Fee", "amount": 50000, "due_date": (today + timedelta(days=3)).strftime("%Y-%m-%d"), "status": "pending"},
        {"student_id": 1, "fee_type": "Hostel Fee", "amount": 20000, "due_date": (today - timedelta(days=10)).strftime("%Y-%m-%d"), "status": "pending"},
        
        # Student 3: Has a transportation fee overdue by 2 days (₹100 penalty)
        {"student_id": 3, "fee_type": "Transport Fee", "amount": 5000, "due_date": (today - timedelta(days=2)).strftime("%Y-%m-%d"), "status": "pending"}
    ]
    db.fees.insert_many(fees_data)

    print("Database seeded successfully with varied test profiles.")

if __name__ == "__main__":
    seed_database()
