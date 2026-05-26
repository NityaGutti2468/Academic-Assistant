from datetime import datetime
from database import fees, students
from services.notification_service import send_sms


def check_fees():

    reminders = []

    for f in fees.find():

        f.pop("_id", None)

        due_date = datetime.strptime(f["due_date"], "%Y-%m-%d")
        today = datetime.now()

        days_left = (due_date - today).days

        student = students.find_one({"student_id": f["student_id"]})

        # ---------- UPCOMING DUE ----------
        if f["status"] == "pending" and 0 <= days_left <= 5:

            message = f"""
FEE REMINDER

Student: {student['name']}
Fee Type: {f['fee_type']}
Amount: ₹{f['amount']}
Due Date: {f['due_date']}

Please pay before due date.
"""

            send_sms(student["parent_phone"], message)

            reminders.append({
                "student_id": f["student_id"],
                "type": "REMINDER",
                "days_left": days_left
            })

        # ---------- OVERDUE ----------
        elif f["status"] == "pending" and days_left < 0:
            
            days_overdue = abs(days_left)
            late_penalty = days_overdue * 50  # ₹50 per day penalty
            total_payable = f['amount'] + late_penalty

            message = f"""
URGENT FEE ALERT

Student: {student['name']}
Fee Type: {f['fee_type']}
Original Amount: ₹{f['amount']}
Late Penalty: ₹{late_penalty} (₹50/day for {days_overdue} days)
Total Payable: ₹{total_payable}

Due Date Passed! Please pay immediately.
"""

            send_sms(student["parent_phone"], message)

            reminders.append({
                "student_id": f["student_id"],
                "type": "OVERDUE",
                "penalty": late_penalty
            })

    return reminders

def get_student_fees(student_id):
    student_id = int(student_id)
    student_fees = list(fees.find({"student_id": student_id, "status": "pending"}))
    
    if not student_fees:
        return {"message": "You have no pending fees.", "data": []}
    
    total_due = 0
    detailed_fees = []
    
    for f in student_fees:
        f.pop("_id", None)
        due_date = datetime.strptime(f["due_date"], "%Y-%m-%d")
        days_left = (due_date - datetime.now()).days
        
        penalty = 0
        if days_left < 0:
            penalty = abs(days_left) * 50
            
        payable = f["amount"] + penalty
        total_due += payable
        
        detailed_fees.append({
            "type": f["fee_type"], 
            "original_amount": f["amount"], 
            "penalty": penalty,
            "total_payable": payable,
            "due_date": f["due_date"]
        })
    
    return {
        "message": f"You have {len(student_fees)} pending fee(s) totaling ₹{total_due} (including late penalties).", 
        "data": detailed_fees
    }