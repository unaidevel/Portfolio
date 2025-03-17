from django.core.mail import send_mail
from django.conf import settings


def send_budget_alert(user_email, budget_name, remaining_amount):
    subject = "Budget Alert: Running low"
    message = f"Your budget '{budget_name}' is running low. Only {remaining_amount} remains!"

    send_mail(
        subject,
        message,
        settings.DEFAUL_FROM_EMAIL,
        [user_email],
        fail_silently=False,
    )