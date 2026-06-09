from datetime import datetime, timedelta

from pymongo import MongoClient


client = MongoClient("mongodb://localhost:27017")
db = client["college_ai"]


def seed_database():
    db.students.delete_many({})
    db.attendance.delete_many({})
    db.marks.delete_many({})
    db.academic_summary.delete_many({})
    db.fees.delete_many({})
    db.alert_logs.delete_many({})
    db.mentors.delete_many({})
    db.courses.delete_many({})
    db.assignments.delete_many({})
    db.student_notes.delete_many({})
    db.scholarships.delete_many({})
    db.fee_payments.delete_many({})
    db.semester_results.delete_many({})

    mentors = [
        {
            "mentor_id": 101,
            "name": "Dr. Kavitha Rao",
            "department": "Artificial Intelligence and Data Science",
            "designation": "Associate Professor",
            "phone": "+919876543211",
            "email": "kavitha.rao@college.edu",
            "office": "AI Block 204",
            "specialization": ["Deep Learning", "Student Counseling", "Research Projects"],
        },
        {
            "mentor_id": 102,
            "name": "Prof. Arjun Menon",
            "department": "Electronics and Communication",
            "designation": "Assistant Professor",
            "phone": "+919876543212",
            "email": "arjun.menon@college.edu",
            "office": "ECE Block 118",
            "specialization": ["Embedded Systems", "IoT", "Academic Remediation"],
        },
        {
            "mentor_id": 103,
            "name": "Dr. Nisha Patel",
            "department": "Computer Science",
            "designation": "Professor",
            "phone": "+919876543215",
            "email": "nisha.patel@college.edu",
            "office": "CSE Block 301",
            "specialization": ["Full Stack Development", "Career Guidance", "RAG Systems"],
        },
    ]
    db.mentors.insert_many(mentors)

    students = [
        {
            "student_id": 1,
            "admission_no": "105/AIM/2023",
            "roll_no": "23A81A6120",
            "name": "Gutti N D Siva Naga Lakshmi Durga",
            "department": "Artificial Intelligence and Machine Learning",
            "program": "B.Tech",
            "course": "B.Tech",
            "branch": "Artificial Intelligence and Machine Learning",
            "semester": 6,
            "section": "A",
            "gender": "Female",
            "dob": "2005-11-04",
            "nationality": "Indian",
            "religion": "Hindu",
            "entrance_type": "EAPCET",
            "cet_rank": "23373",
            "seat_type": "CONVENOR",
            "last_studied": "Vasavi Vignan Junior College",
            "joining_date": "2023-08-28",
            "email": "student6120@college.edu",
            "college_email": "23A81A6120@sves.org.in",
            "phone": "+916302505590",
            "abc_id": "341066381362",
            "bank_account_no": "XXXXXX2292",
            "aadhaar_no": "XXXX-XXXX-9911",
            "reimbursement": "Yes",
            "transport_halt": "Siddantham",
            "parent_name": "Gutti Ramakrishna",
            "parent_phone": "+919876543210",
            "parent_details": {
                "father_name": "Gutti Ramakrishna",
                "father_occupation": "Farmer",
                "father_mobile": "+918328224313",
                "mother_name": "Gutti Krishna Veni",
                "mother_occupation": "House Wife",
                "mother_mobile": "+916300717696",
                "annual_income": 72000,
                "correspondence_address": "Penugonda, West Godavari, Andhra Pradesh",
                "permanent_address": "Penugonda, West Godavari, Andhra Pradesh",
            },
            "education_details": [
                {
                    "qualification": "S.S.C",
                    "board": "Board of Secondary Education",
                    "hall_ticket_no": "2110107463",
                    "year_of_pass": 2021,
                    "institute": "ZPP High School",
                    "max_marks": 600,
                    "obtained_marks": 553,
                    "percentage": 92.17,
                },
                {
                    "qualification": "Inter",
                    "board": "Board of Intermediate Education",
                    "hall_ticket_no": "2304241448",
                    "year_of_pass": 2023,
                    "institute": "Vasavi Vignan Junior College",
                    "max_marks": 1000,
                    "obtained_marks": 969,
                    "percentage": 96.90,
                },
            ],
            "address": "Penugonda, Andhra Pradesh",
            "admission_year": 2023,
            "mentor_id": 101,
            "status": "active",
            "learning_profile": {
                "preferred_language": "English",
                "learning_style": "visual",
                "career_goal": "AI Engineer",
                "risk_tags": ["low_attendance", "fee_pending"],
            },
        },
        {
            "student_id": 2,
            "roll_no": "23AI002",
            "name": "Maria Garcia",
            "department": "Artificial Intelligence and Data Science",
            "program": "B.Tech",
            "semester": 5,
            "section": "A",
            "email": "maria.garcia@student.college.edu",
            "phone": "+919000000002",
            "parent_name": "Elena Garcia",
            "parent_phone": "+919876543213",
            "address": "Bengaluru, Karnataka",
            "admission_year": 2023,
            "mentor_id": 101,
            "status": "active",
            "learning_profile": {
                "preferred_language": "English",
                "learning_style": "practice",
                "career_goal": "Data Scientist",
                "risk_tags": [],
            },
        },
        {
            "student_id": 3,
            "roll_no": "23EC014",
            "name": "David Chen",
            "department": "Electronics and Communication",
            "program": "B.Tech",
            "semester": 5,
            "section": "B",
            "email": "david.chen@student.college.edu",
            "phone": "+919000000003",
            "parent_name": "Linda Chen",
            "parent_phone": "+919876543214",
            "address": "Chennai, Tamil Nadu",
            "admission_year": 2023,
            "mentor_id": 102,
            "status": "active",
            "learning_profile": {
                "preferred_language": "English",
                "learning_style": "guided",
                "career_goal": "Embedded Systems Engineer",
                "risk_tags": ["academic_warning", "low_attendance", "fee_pending"],
            },
        },
        {
            "student_id": 4,
            "roll_no": "23CS021",
            "name": "Priya Sharma",
            "department": "Computer Science",
            "program": "B.Tech",
            "semester": 5,
            "section": "C",
            "email": "priya.sharma@student.college.edu",
            "phone": "+919000000004",
            "parent_name": "Anil Sharma",
            "parent_phone": "+919876543216",
            "address": "Pune, Maharashtra",
            "admission_year": 2023,
            "mentor_id": 103,
            "status": "active",
            "learning_profile": {
                "preferred_language": "English",
                "learning_style": "project_based",
                "career_goal": "Full Stack Developer",
                "risk_tags": ["placement_ready"],
            },
        },
    ]

    extra_students = [
        ("23AI005", "Rahul Verma", "Artificial Intelligence and Machine Learning", "B.Tech", 6, "A", "Male", 101, "Data Engineer", 82.0, 8.1, 8.3, 0),
        ("23AI006", "Sneha Reddy", "Artificial Intelligence and Machine Learning", "B.Tech", 6, "A", "Female", 101, "ML Engineer", 91.0, 9.2, 9.0, 0),
        ("23CS007", "Arjun Kumar", "Computer Science", "B.Tech", 6, "B", "Male", 103, "Backend Developer", 76.0, 7.4, 7.6, 0),
        ("23CS008", "Meera Iyer", "Computer Science", "B.Tech", 6, "B", "Female", 103, "Product Engineer", 68.0, 6.3, 6.7, 1),
        ("23EC009", "Farhan Ali", "Electronics and Communication", "B.Tech", 6, "C", "Male", 102, "IoT Engineer", 73.0, 6.8, 7.0, 0),
        ("23EC010", "Kavya Nair", "Electronics and Communication", "B.Tech", 6, "C", "Female", 102, "Embedded Systems Engineer", 96.0, 9.5, 9.3, 0),
    ]

    for index, (roll_no, name, branch, course, semester, section, gender, mentor_id, career_goal, attendance_percent, sgpa, cgpa, backlogs) in enumerate(extra_students, start=5):
        students.append({
            "student_id": index,
            "admission_no": f"{100 + index}/GEN/2023",
            "roll_no": roll_no,
            "name": name,
            "department": branch,
            "program": course,
            "course": course,
            "branch": branch,
            "semester": semester,
            "section": section,
            "gender": gender,
            "dob": f"2005-{(index % 9) + 1:02d}-{(index * 3) % 27 + 1:02d}",
            "nationality": "Indian",
            "religion": "Not specified",
            "entrance_type": "EAPCET",
            "cet_rank": str(18000 + index * 913),
            "seat_type": "CONVENOR",
            "last_studied": "State Junior College",
            "joining_date": "2023-08-28",
            "email": f"{roll_no.lower()}@student.college.edu",
            "college_email": f"{roll_no.lower()}@sves.org.in",
            "phone": f"+9190000000{index:02d}",
            "abc_id": f"34106638{index:04d}",
            "bank_account_no": f"XXXXXX{2200 + index}",
            "aadhaar_no": f"XXXX-XXXX-{9900 + index}",
            "reimbursement": "Yes" if index % 2 == 0 else "No",
            "transport_halt": "Campus" if index % 2 == 0 else "Town Bus Stop",
            "parent_name": f"Parent of {name}",
            "parent_phone": f"+9198765432{10 + index}",
            "parent_details": {
                "father_name": f"Father of {name}",
                "father_occupation": "Private Employee",
                "father_mobile": f"+9183282243{index:02d}",
                "mother_name": f"Mother of {name}",
                "mother_occupation": "Homemaker",
                "mother_mobile": f"+9163007176{index:02d}",
                "annual_income": 120000 + index * 15000,
                "correspondence_address": "Andhra Pradesh",
                "permanent_address": "Andhra Pradesh",
            },
            "education_details": [
                {
                    "qualification": "S.S.C",
                    "board": "Board of Secondary Education",
                    "hall_ticket_no": f"2110107{index:03d}",
                    "year_of_pass": 2021,
                    "institute": "ZP High School",
                    "max_marks": 600,
                    "obtained_marks": int(480 + index * 7),
                    "percentage": round((480 + index * 7) / 600 * 100, 2),
                },
                {
                    "qualification": "Inter",
                    "board": "Board of Intermediate Education",
                    "hall_ticket_no": f"2304241{index:03d}",
                    "year_of_pass": 2023,
                    "institute": "State Junior College",
                    "max_marks": 1000,
                    "obtained_marks": int(780 + index * 11),
                    "percentage": round((780 + index * 11) / 1000 * 100, 2),
                },
            ],
            "address": "Andhra Pradesh",
            "admission_year": 2023,
            "mentor_id": mentor_id,
            "status": "active",
            "learning_profile": {
                "preferred_language": "English",
                "learning_style": "project_based" if sgpa >= 8 else "guided",
                "career_goal": career_goal,
                "risk_tags": [
                    tag
                    for tag, enabled in {
                        "low_attendance": attendance_percent < 75,
                        "academic_warning": sgpa < 6.5 or backlogs > 0,
                        "fee_pending": index in (5, 8, 9),
                        "placement_ready": sgpa >= 9,
                    }.items()
                    if enabled
                ],
            },
        })
    db.students.insert_many(students)

    courses = [
        {"course_code": "V23AIT04", "course_name": "Computer Networks", "department": "AI&DS", "semester": 5, "credits": 3.0, "faculty": "Dr. Kavitha Rao"},
        {"course_code": "V23AIT03", "course_name": "Deep Learning", "department": "AI&DS", "semester": 5, "credits": 3.0, "faculty": "Dr. Kavitha Rao"},
        {"course_code": "V23MLT01", "course_name": "Natural Language Processing", "department": "AI&DS", "semester": 5, "credits": 3.0, "faculty": "Dr. Nisha Patel"},
        {"course_code": "V23CSSE03", "course_name": "Full Stack Development-II", "department": "CSE", "semester": 5, "credits": 2.0, "faculty": "Dr. Nisha Patel"},
        {"course_code": "V23ECT05", "course_name": "Embedded Systems", "department": "ECE", "semester": 5, "credits": 3.0, "faculty": "Prof. Arjun Menon"},
    ]
    db.courses.insert_many(courses)

    attendance = [
        {
            "student_id": 1,
            "total_classes": 100,
            "attended_classes": 70,
            "percentage": 70.0,
            "last_updated": datetime.now().strftime("%Y-%m-%d"),
            "subject_breakdown": [
                {"course_code": "V23AIT04", "held": 25, "attended": 18, "percentage": 72.0},
                {"course_code": "V23AIT03", "held": 25, "attended": 16, "percentage": 64.0},
                {"course_code": "V23MLT01", "held": 25, "attended": 19, "percentage": 76.0},
                {"course_code": "V23CSSE03", "held": 25, "attended": 17, "percentage": 68.0},
            ],
        },
        {"student_id": 2, "total_classes": 100, "attended_classes": 95, "percentage": 95.0, "last_updated": datetime.now().strftime("%Y-%m-%d")},
        {"student_id": 3, "total_classes": 100, "attended_classes": 60, "percentage": 60.0, "last_updated": datetime.now().strftime("%Y-%m-%d")},
        {"student_id": 4, "total_classes": 100, "attended_classes": 88, "percentage": 88.0, "last_updated": datetime.now().strftime("%Y-%m-%d")},
    ]
    for student in students[4:]:
        pct = next(item[9] for item in extra_students if item[0] == student["roll_no"])
        attendance.append({
            "student_id": student["student_id"],
            "total_classes": 100,
            "attended_classes": int(pct),
            "percentage": pct,
            "last_updated": datetime.now().strftime("%Y-%m-%d"),
        })
    db.attendance.insert_many(attendance)

    marks_data = [
        {"student_id": 1, "course_code": "V23AIT04", "subject": "COMPUTER NETWORKS", "marks": 85, "credits": 3.0, "exam_type": "Final", "semester": 5},
        {"student_id": 1, "course_code": "V23AIT03", "subject": "DEEP LEARNING", "marks": 92, "credits": 3.0, "exam_type": "Final", "semester": 5},
        {"student_id": 1, "course_code": "V23MLT01", "subject": "NATURAL LANGUAGE PROCESSING", "marks": 88, "credits": 3.0, "exam_type": "Final", "semester": 5},
        {"student_id": 1, "course_code": "V23CSSE03", "subject": "FULL STACK DEVELOPMENT-II", "marks": 96, "credits": 2.0, "exam_type": "Final", "semester": 5},
        {"student_id": 2, "course_code": "V23AIT04", "subject": "COMPUTER NETWORKS", "marks": 90, "credits": 3.0, "exam_type": "Final", "semester": 5},
        {"student_id": 2, "course_code": "V23AIT03", "subject": "DEEP LEARNING", "marks": 80, "credits": 3.0, "exam_type": "Final", "semester": 5},
        {"student_id": 2, "course_code": "V23CSSE03", "subject": "FULL STACK DEVELOPMENT-II", "marks": 95, "credits": 2.0, "exam_type": "Final", "semester": 5},
        {"student_id": 3, "course_code": "V23AIT04", "subject": "COMPUTER NETWORKS", "marks": 35, "credits": 3.0, "exam_type": "Final", "semester": 5},
        {"student_id": 3, "course_code": "V23AIT03", "subject": "DEEP LEARNING", "marks": 40, "credits": 3.0, "exam_type": "Final", "semester": 5},
        {"student_id": 3, "course_code": "V23ECT05", "subject": "EMBEDDED SYSTEMS", "marks": 52, "credits": 3.0, "exam_type": "Final", "semester": 5},
        {"student_id": 4, "course_code": "V23AIT03", "subject": "DEEP LEARNING", "marks": 89, "credits": 3.0, "exam_type": "Final", "semester": 5},
        {"student_id": 4, "course_code": "V23MLT01", "subject": "NATURAL LANGUAGE PROCESSING", "marks": 91, "credits": 3.0, "exam_type": "Final", "semester": 5},
        {"student_id": 4, "course_code": "V23CSSE03", "subject": "FULL STACK DEVELOPMENT-II", "marks": 98, "credits": 2.0, "exam_type": "Final", "semester": 5},
    ]
    common_subjects = [
        ("V23AIT03", "DEEP LEARNING", 3.0),
        ("V23MLT01", "NATURAL LANGUAGE PROCESSING", 3.0),
        ("V23CSSE03", "FULL STACK DEVELOPMENT-II", 2.0),
        ("V23AIT04", "COMPUTER NETWORKS", 3.0),
    ]
    for student in students[4:]:
        profile = next(item for item in extra_students if item[0] == student["roll_no"])
        sgpa = profile[10]
        base_mark = int(min(96, max(52, sgpa * 10 - 4)))
        for offset, (course_code, subject, credits) in enumerate(common_subjects):
            marks_data.append({
                "student_id": student["student_id"],
                "course_code": course_code,
                "subject": subject,
                "marks": max(35, min(99, base_mark + offset * 2 - 3)),
                "credits": credits,
                "exam_type": "Final",
                "semester": 5,
            })
    db.marks.insert_many(marks_data)

    semester_results = [
        {
            "student_id": 1,
            "semester_no": 2,
            "semester_label": "II Semester",
            "exam_month": "Jun-24",
            "courses": [
                {"s_no": 1, "course_code": "V23MAT02", "course_name": "DIFFERENTIAL EQUATIONS & VECTOR CALCULUS", "grade": "S", "grade_points": 10, "credits": 3.0, "result": "P"},
                {"s_no": 2, "course_code": "V23PHT01", "course_name": "ENGINEERING PHYSICS", "grade": "A", "grade_points": 9, "credits": 3.0, "result": "P"},
                {"s_no": 3, "course_code": "V23ENT01", "course_name": "COMMUNICATIVE ENGLISH", "grade": "C", "grade_points": 7, "credits": 2.0, "result": "P"},
                {"s_no": 4, "course_code": "V23EET01", "course_name": "BASIC ELECTRICAL & ELECTRONICS ENGINEERING", "grade": "S", "grade_points": 10, "credits": 3.0, "result": "P"},
                {"s_no": 5, "course_code": "V23CST02", "course_name": "DATA STRUCTURES", "grade": "S", "grade_points": 10, "credits": 3.0, "result": "P"},
                {"s_no": 6, "course_code": "V23EPL01", "course_name": "ENGINEERING PHYSICS LAB", "grade": "S", "grade_points": 10, "credits": 1.0, "result": "P"},
                {"s_no": 7, "course_code": "V23ENL01", "course_name": "COMMUNICATIVE ENGLISH LAB", "grade": "S", "grade_points": 10, "credits": 1.0, "result": "P"},
                {"s_no": 8, "course_code": "V23EEL01", "course_name": "ELECTRICAL & ELECTRONICS ENGINEERING WORKSHOP", "grade": "A", "grade_points": 9, "credits": 1.5, "result": "P"},
                {"s_no": 9, "course_code": "V23CSL03", "course_name": "DATA STRUCTURES LAB", "grade": "S", "grade_points": 10, "credits": 1.5, "result": "P"},
                {"s_no": 10, "course_code": "V23SPT02", "course_name": "HEALTH AND WELLNESS, YOGA AND SPORTS", "grade": "B", "grade_points": 8, "credits": 0.5, "result": "P"},
            ],
            "passed_count": 10,
            "failed_count": 0,
            "overall_result": "Pass",
            "sgpa": 9.41,
            "percentage": 86.60,
            "total_grade_points": 183.5,
            "total_credits": 19.5,
        },
        {
            "student_id": 1,
            "semester_no": 3,
            "semester_label": "III Semester",
            "exam_month": "Dec-24",
            "courses": [
                {"s_no": 1, "course_code": "V23MAT05", "course_name": "DISCRETE MATHEMATICS AND GRAPH THEORY", "grade": "S", "grade_points": 10, "credits": 3.0, "result": "P"},
                {"s_no": 2, "course_code": "V23MBT53", "course_name": "UNIVERSAL HUMAN VALUES", "grade": "C", "grade_points": 7, "credits": 3.0, "result": "P"},
                {"s_no": 3, "course_code": "V23AIT01", "course_name": "ARTIFICIAL INTELLIGENCE", "grade": "B", "grade_points": 8, "credits": 3.0, "result": "P"},
                {"s_no": 4, "course_code": "V23CST04", "course_name": "ADVANCED DATA STRUCTURES AND ALGORITHM ANALYSIS", "grade": "A", "grade_points": 9, "credits": 3.0, "result": "P"},
                {"s_no": 5, "course_code": "V23CST05", "course_name": "OBJECT ORIENTED PROGRAMMING THROUGH JAVA", "grade": "A", "grade_points": 9, "credits": 3.0, "result": "P"},
                {"s_no": 6, "course_code": "V23CSL04", "course_name": "ADVANCED DATA STRUCTURES AND ALGORITHMS ANALYSIS LAB", "grade": "A", "grade_points": 9, "credits": 1.5, "result": "P"},
                {"s_no": 7, "course_code": "V23CSL05", "course_name": "OBJECT ORIENTED PROGRAMMING THROUGH JAVA LAB", "grade": "S", "grade_points": 10, "credits": 1.5, "result": "P"},
                {"s_no": 8, "course_code": "V23CSSE01", "course_name": "PYTHON PROGRAMMING LAB", "grade": "A", "grade_points": 9, "credits": 2.0, "result": "P"},
                {"s_no": 9, "course_code": "V23MET09", "course_name": "DESIGN THINKING AND INNOVATION", "grade": "S", "grade_points": 10, "credits": 2.0, "result": "P"},
            ],
            "passed_count": 9,
            "failed_count": 0,
            "overall_result": "Pass",
            "sgpa": 8.89,
            "percentage": 81.36,
            "total_grade_points": 195.5,
            "total_credits": 22.0,
        },
    ]
    for student in students[1:]:
        summary_profile = None
        if student["student_id"] >= 5:
            summary_profile = next(item for item in extra_students if item[0] == student["roll_no"])
            sgpa = summary_profile[10]
        else:
            sgpa = {2: 9.0, 3: 4.8, 4: 9.4}.get(student["student_id"], 7.0)

        grade = "S" if sgpa >= 9 else "A" if sgpa >= 8 else "B" if sgpa >= 7 else "C" if sgpa >= 6 else "F"
        grade_points = {"S": 10, "A": 9, "B": 8, "C": 7, "F": 0}[grade]
        result = "P" if grade != "F" else "F"
        credits = [3.0, 3.0, 3.0, 2.0, 1.5]
        generated_courses = []
        for course_index, (course_code, course_name, course_credits) in enumerate([
            ("V23AIT03", "DEEP LEARNING", credits[0]),
            ("V23MLT01", "NATURAL LANGUAGE PROCESSING", credits[1]),
            ("V23AIT04", "COMPUTER NETWORKS", credits[2]),
            ("V23CSSE03", "FULL STACK DEVELOPMENT-II", credits[3]),
            ("V23CSL05", "PYTHON PROGRAMMING LAB", credits[4]),
        ], start=1):
            generated_courses.append({
                "s_no": course_index,
                "course_code": course_code,
                "course_name": course_name,
                "grade": grade,
                "grade_points": grade_points,
                "credits": course_credits,
                "result": result,
            })

        total_credits = sum(item["credits"] for item in generated_courses)
        total_grade_points = sum(item["grade_points"] * item["credits"] for item in generated_courses)
        failed_count = 0 if result == "P" else len(generated_courses)
        semester_results.append({
            "student_id": student["student_id"],
            "semester_no": 5,
            "semester_label": "V Semester",
            "exam_month": "Nov-25",
            "courses": generated_courses,
            "passed_count": len(generated_courses) - failed_count,
            "failed_count": failed_count,
            "overall_result": "Pass" if failed_count == 0 else "Fail",
            "sgpa": round(total_grade_points / total_credits, 2) if total_credits else 0,
            "percentage": round((total_grade_points / total_credits) * 10 - 7.5, 2) if total_credits else 0,
            "total_grade_points": round(total_grade_points, 2),
            "total_credits": total_credits,
        })
    db.semester_results.insert_many(semester_results)

    summary_data = [
        {"student_id": 1, "cgpa": 9.3, "sgpa": 9.5, "backlogs": 0, "credits_earned": 94, "academic_standing": "Excellent"},
        {"student_id": 2, "cgpa": 8.8, "sgpa": 9.0, "backlogs": 0, "credits_earned": 98, "academic_standing": "Excellent"},
        {"student_id": 3, "cgpa": 5.2, "sgpa": 4.8, "backlogs": 2, "credits_earned": 72, "academic_standing": "Critical"},
        {"student_id": 4, "cgpa": 9.1, "sgpa": 9.4, "backlogs": 0, "credits_earned": 101, "academic_standing": "Placement Ready"},
    ]
    for student in students[4:]:
        profile = next(item for item in extra_students if item[0] == student["roll_no"])
        sgpa = profile[10]
        cgpa = profile[11]
        backlogs = profile[12]
        summary_data.append({
            "student_id": student["student_id"],
            "cgpa": cgpa,
            "sgpa": sgpa,
            "backlogs": backlogs,
            "credits_earned": int(80 + sgpa * 3),
            "academic_standing": "Excellent" if sgpa >= 9 else "Good" if sgpa >= 7 else "Warning",
        })
    db.academic_summary.insert_many(summary_data)

    assignments = [
        {"student_id": 1, "course_code": "V23AIT03", "title": "CNN Mini Project", "score": 82, "max_score": 100, "status": "submitted"},
        {"student_id": 1, "course_code": "V23MLT01", "title": "Text Classifier Lab", "score": 76, "max_score": 100, "status": "submitted"},
        {"student_id": 3, "course_code": "V23AIT03", "title": "Backpropagation Worksheet", "score": 38, "max_score": 100, "status": "needs_resubmission"},
        {"student_id": 4, "course_code": "V23CSSE03", "title": "React ERP Dashboard", "score": 96, "max_score": 100, "status": "submitted"},
    ]
    db.assignments.insert_many(assignments)

    today = datetime.now()
    fees_data = [
        {"student_id": 1, "fee_type": "Tuition Fee", "amount": 50000, "due_date": (today + timedelta(days=3)).strftime("%Y-%m-%d"), "status": "pending", "semester": 5},
        {"student_id": 1, "fee_type": "Hostel Fee", "amount": 20000, "due_date": (today - timedelta(days=10)).strftime("%Y-%m-%d"), "status": "pending", "semester": 5},
        {"student_id": 3, "fee_type": "Transport Fee", "amount": 5000, "due_date": (today - timedelta(days=2)).strftime("%Y-%m-%d"), "status": "pending", "semester": 5},
        {"student_id": 4, "fee_type": "Exam Fee", "amount": 2500, "due_date": (today + timedelta(days=20)).strftime("%Y-%m-%d"), "status": "paid", "semester": 5},
    ]
    for student_id in (5, 8, 9):
        fees_data.append({
            "student_id": student_id,
            "fee_type": "Tuition Fee",
            "amount": 30000,
            "due_date": (today + timedelta(days=5 - student_id)).strftime("%Y-%m-%d"),
            "status": "pending",
            "semester": 6,
        })
    db.fees.insert_many(fees_data)

    fee_payments = [
        {"student_id": 2, "receipt_no": "RCPT-2026-0021", "fee_type": "Tuition Fee", "amount": 50000, "paid_on": (today - timedelta(days=12)).strftime("%Y-%m-%d"), "mode": "UPI"},
        {"student_id": 4, "receipt_no": "RCPT-2026-0024", "fee_type": "Exam Fee", "amount": 2500, "paid_on": (today - timedelta(days=1)).strftime("%Y-%m-%d"), "mode": "Card"},
    ]
    db.fee_payments.insert_many(fee_payments)

    student_notes = [
        {"student_id": 1, "mentor_id": 101, "note_type": "attendance_plan", "note": "Attend all Deep Learning sessions for the next two weeks.", "created_at": today.strftime("%Y-%m-%d")},
        {"student_id": 3, "mentor_id": 102, "note_type": "academic_remediation", "note": "Schedule weekly remedial sessions for Computer Networks and Deep Learning.", "created_at": today.strftime("%Y-%m-%d")},
        {"student_id": 4, "mentor_id": 103, "note_type": "placement", "note": "Recommended for full-stack internship applications.", "created_at": today.strftime("%Y-%m-%d")},
    ]
    db.student_notes.insert_many(student_notes)

    scholarships = [
        {"student_id": 2, "name": "Merit Scholarship", "amount": 15000, "status": "approved", "renewal_due": "2026-07-15"},
        {"student_id": 4, "name": "Women in Tech Grant", "amount": 20000, "status": "approved", "renewal_due": "2026-08-01"},
    ]
    db.scholarships.insert_many(scholarships)

    alert_logs = [
        {"student_id": 1, "type": "Low Attendance", "severity": "High", "message": "Attendance is below 75%.", "created_at": today.strftime("%Y-%m-%d"), "status": "open"},
        {"student_id": 3, "type": "Academic Warning", "severity": "High", "message": "CGPA below 6 with active backlogs.", "created_at": today.strftime("%Y-%m-%d"), "status": "open"},
        {"student_id": 3, "type": "Fee Pending", "severity": "Medium", "message": "Transport fee is overdue.", "created_at": today.strftime("%Y-%m-%d"), "status": "open"},
    ]
    for student in students[4:]:
        risk_tags = student["learning_profile"]["risk_tags"]
        if "low_attendance" in risk_tags:
            alert_logs.append({"student_id": student["student_id"], "type": "Low Attendance", "severity": "High", "message": "Attendance is below 75%.", "created_at": today.strftime("%Y-%m-%d"), "status": "open"})
        if "academic_warning" in risk_tags:
            alert_logs.append({"student_id": student["student_id"], "type": "Academic Warning", "severity": "Medium", "message": "Student needs academic mentoring.", "created_at": today.strftime("%Y-%m-%d"), "status": "open"})
        if "fee_pending" in risk_tags:
            alert_logs.append({"student_id": student["student_id"], "type": "Fee Pending", "severity": "Medium", "message": "Pending fee follow-up required.", "created_at": today.strftime("%Y-%m-%d"), "status": "open"})
    db.alert_logs.insert_many(alert_logs)

    print("Database seeded successfully with enriched academic profiles.")


if __name__ == "__main__":
    seed_database()
