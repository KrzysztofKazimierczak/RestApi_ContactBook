from pathlib import Path

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from fastapi_mail.errors import ConnectionErrors
from pydantic import EmailStr

from services.auth import auth_service

conf = ConnectionConfig(
    MAIL_USERNAME='test.python.3.group@gmail.com',
    MAIL_PASSWORD='cicy nlog qten zgvk',
    MAIL_FROM='test.python.3.group@gmail.com',
    MAIL_PORT=587,
    MAIL_SERVER='smtp.gmail.com',
    MAIL_FROM_NAME="Test Python",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(__file__).parent / 'templates',

)

async def send_email(email: EmailStr, username: str, host: str):
    try:
        token_verification = auth_service.create_email_token({"sub": email})
        message = MessageSchema(
            subject="Confirm your email ",
            recipients=[email],
            template_body={"host": host, "username": username, "token": token_verification},
            subtype=MessageType.html
        )

        fm = FastMail(conf)
        await fm.send_message(message, template_name="email_template.html")
    except ConnectionErrors as err:
        print(err)
