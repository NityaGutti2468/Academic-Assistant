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

print("MongoDB Connected")