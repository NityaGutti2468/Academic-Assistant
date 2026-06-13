import os

from pymongo import MongoClient


mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
mongo_db = os.getenv("MONGO_DB", "college_ai")

client = MongoClient(
    mongo_uri,
    serverSelectionTimeoutMS=int(os.getenv("MONGO_TIMEOUT_MS", "5000")),
)

db = client[mongo_db]

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
