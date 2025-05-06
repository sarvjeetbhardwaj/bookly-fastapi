from fastapi_mail import FastMail, ConnectionConfig, MessageSchema,MessageType
from src.config import config
from pathlib import Path
import os


mail_conf = ConnectionConfig(
    MAIL_USERNAME = os.getenv('MAIL_USERNAME'),
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD'),
    MAIL_FROM = 'sjitbh121993@gmail.com',
    MAIL_PORT = 587,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS =True,
    VALIDATE_CERTS = False,
    TEMPLATE_FOLDER=Path('./src/templates')
)

mail = FastMail(config=mail_conf)

def create_message(recepients:list[str],subject:str, body:str):
    message = MessageSchema(
        recipients=recepients, 
        subject=subject,
        body=body,
        subtype=MessageType.html
    )

    return message
