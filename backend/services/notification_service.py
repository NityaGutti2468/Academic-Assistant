from twilio.rest import Client
import os
from dotenv import load_dotenv
from database import alert_logs
from datetime import datetime, timedelta

load_dotenv()

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_phone = os.getenv("TWILIO_PHONE")

client = Client(account_sid, auth_token)


def send_sms(phone_number, message):

    try:
        # Prevent Duplicate: check if exact message sent in last 24 hours
        time_threshold = datetime.now() - timedelta(hours=24)
        duplicate = alert_logs.find_one({
            "phone_number": phone_number,
            "message": message,
            "timestamp": {"$gte": time_threshold}
        })
        
        if duplicate:
            print("Skipping duplicate SMS to", phone_number)
            return

        # Ensure phone number is in international format
        if not phone_number.startswith("+"):
            phone_number = "+91" + phone_number

        msg = client.messages.create(
            body=message,
            from_=twilio_phone,
            to=phone_number
        )

        print("SMS sent:", msg.sid)
        
        # Log to prevent future duplicates
        alert_logs.insert_one({
            "phone_number": phone_number,
            "message": message,
            "timestamp": datetime.now()
        })

    except Exception as e:
        print("SMS error:", e)