import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SMTP_FROM = os.getenv("SMTP_FROM", SMTP_USER or "")


def _send_email(recipient, subject, body):
    if not SMTP_USER or not SMTP_PASSWORD or not SMTP_FROM:
        raise RuntimeError(
            "SMTP configuration is missing. Set SMTP_USER, SMTP_PASSWORD and optionally SMTP_FROM."
        )

    msg = MIMEMultipart()
    msg["From"] = SMTP_FROM
    msg["To"] = recipient
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(SMTP_FROM, recipient, msg.as_string())


def sendMailSoftwareOwner(email, verificationKey):
    admin_email = os.getenv("SOFTWARE_OWNER_ADMIN_EMAIL", SMTP_FROM)
    subject = "Verification Code for Coma Gen-e"
    body = (
        "Hello, welcome to Coma Gen-e. "
        f"Verification code: {verificationKey}. "
        f"Software owner email: {email}"
    )
    _send_email(admin_email, subject, body)


def sendMail(recipient, verificationKey):
    subject = "Verification Code for Coma Gen-e"
    body = f"Hello, welcome to Coma Gen-e. Your verification code is: {verificationKey}"
    _send_email(recipient, subject, body)
