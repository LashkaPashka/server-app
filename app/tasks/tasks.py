from app.tasks.app_celery import celery
from pydantic import EmailStr
import smtplib
from app.config import settings
from app.tasks.email_send import create_email_letter





@celery.task
def send_email(booking: dict,  email_user: EmailStr):

    get_content = create_email_letter(booking, email_user)

    with smtplib.SMTP_SSL(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
        server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        server.send_message(get_content)





