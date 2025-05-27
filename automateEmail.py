import smtplib
import os
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

def send_reset_email(to_email, reset_code):
    from_email = os.getenv("GMAIL_USER")
    app_password = os.getenv("GMAIL_APP_PASSWORD")

    body = f"Hi,\n\nYour password reset code is: {reset_code}\n\nRegards,\nPassword Manager"

    msg = MIMEText(body)
    msg["Subject"] = "Password Reset Code"
    msg["From"] = from_email
    msg["To"] = to_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(from_email, app_password)
        server.send_message(msg)
    



