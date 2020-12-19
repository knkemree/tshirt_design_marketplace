from celery import shared_task
from django.core.mail import send_mail
from orders.models import Order

@shared_task
def send_activation_email(user, subject, message):
    print(user, subject, message)
    #user.email_customer(subject, message)



