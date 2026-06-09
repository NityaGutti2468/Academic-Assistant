import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
from database import alert_logs
from datetime import datetime, timedelta
from twilio.rest import Client

load_dotenv()

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_phone = os.getenv("TWILIO_PHONE")

smtp_host = os.getenv("SMTP_HOST")
smtp_port = int(os.getenv("SMTP_PORT", "587"))
smtp_user = os.getenv("SMTP_USER")
smtp_password = os.getenv("SMTP_PASSWORD")
smtp_from = os.getenv("SMTP_FROM") or smtp_user

client = Client(account_sid, auth_token) if account_sid and auth_token else None


def was_recently_sent(channel, recipient, message):
    time_threshold = datetime.now() - timedelta(hours=24)
    return alert_logs.find_one({
        "channel": channel,
        "recipient": recipient,
        "message": message,
        "timestamp": {"$gte": time_threshold}
    })


def log_notification(channel, recipient, message, subject=None):
    alert_logs.insert_one({
        "channel": channel,
        "recipient": recipient,
        "subject": subject,
        "message": message,
        "timestamp": datetime.now()
    })


def send_sms(phone_number, message):

    try:
        if not client or not twilio_phone:
            print("SMS skipped: Twilio credentials are not configured.")
            return False

        if not phone_number:
            print("SMS skipped: phone number is missing.")
            return False

        if was_recently_sent("sms", phone_number, message):
            print("Skipping duplicate SMS to", phone_number)
            return False

        # Ensure phone number is in international format
        if not phone_number.startswith("+"):
            phone_number = "+91" + phone_number

        msg = client.messages.create(
            body=message,
            from_=twilio_phone,
            to=phone_number
        )

        print("SMS sent:", msg.sid)
        log_notification("sms", phone_number, message)
        return True

    except Exception as e:
        print("SMS error:", e)
        return False


def send_email(to_email, subject, message):

    try:
        if not all([smtp_host, smtp_user, smtp_password, smtp_from]):
            print("Email skipped: SMTP credentials are not configured.")
            return False

        if not to_email:
            print("Email skipped: recipient email is missing.")
            return False

        if was_recently_sent("email", to_email, message):
            print("Skipping duplicate email to", to_email)
            return False

        email = EmailMessage()
        email["From"] = smtp_from
        email["To"] = to_email
        email["Subject"] = subject
        email.set_content(message)

        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(email)

        print("Email sent:", to_email)
        log_notification("email", to_email, message, subject)
        return True

    except Exception as e:
        print("Email error:", e)
        return False
