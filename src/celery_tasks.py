from celery import Celery
from src.mail import mail, create_message
from asgiref.sync import async_to_sync

c_app = Celery()

c_app.config_from_object('src.config')

@c_app.task()
def send_email(receipients:list[str], subject:str, body:str):
    message = create_message(recepients=receipients, subject=subject,body=body)

    async_to_sync(mail.send_message)(message=message)
