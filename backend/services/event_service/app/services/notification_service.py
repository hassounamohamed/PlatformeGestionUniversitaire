from fastapi import BackgroundTasks


def send_event_notification(background_tasks: BackgroundTasks, email_to: str, subject: str, body: str):
    # Placeholder: add email sending task here (smtplib or external service)
    # background_tasks.add_task(send_email, email_to, subject, body)
    print(f"Would send notification to {email_to}: {subject}")
