from email.message import EmailMessage
from pydantic import EmailStr
from app.config import settings




def create_email_letter(
        booking: dict,
        email_user: EmailStr
):
    email = EmailMessage()
    email["Subject"] = 'Подтверждение бронирования'
    email['From'] = settings.EMAIL_HOST_USER
    email['To'] = email_user


    email.set_content(

        f'''
        <h1>Подтвердите бронирование</h1>
            Вы забронировали отель с {booking["date_from"]} по {booking["date_to"]}
        ''',
        subtype='html'
    )
    return email

