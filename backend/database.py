from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")

db = client["college_ai"]

students = db["students"]
attendance = db["attendance"]
marks = db["marks"]
academic_summary = db["academic_summary"]
fees = db["fees"]
alert_logs = db["alert_logs"]
mentors = db["mentors"]
courses = db["courses"]
assignments = db["assignments"]
student_notes = db["student_notes"]
scholarships = db["scholarships"]
fee_payments = db["fee_payments"]
semester_results = db["semester_results"]

print("MongoDB Connected")
