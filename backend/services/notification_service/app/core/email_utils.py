import smtplib
from email.message import EmailMessage
from typing import Optional
from app.core.config import settings


def send_email_sync(to: str, subject: str, body: str, html: Optional[str] = None) -> None:
    """Send an email using SMTP synchronously. If SMTP settings are not configured, print to console."""
    host = settings.SMTP_HOST
    if not host:
        # Development fallback
        print("SMTP not configured, printing email to console:")
        print(f"To: {to}\nSubject: {subject}\n{body}")
        return

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = settings.SMTP_FROM
    msg["To"] = to
    if html:
        msg.set_content(body)
        msg.add_alternative(html, subtype="html")
    else:
        msg.set_content(body)

    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as smtp:
        smtp.starttls()
        if settings.SMTP_USER:
            smtp.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        smtp.send_message(msg)
