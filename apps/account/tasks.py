from django.core.mail import send_mail
from config.celery import app
from decouple import config


@app.task
def send_verification_code(email: str, verify_code: str) -> None:
    full_link = f"http://{config('SERVER_IP')}/api/v1/user/verify/{verify_code}/"
    
    send_mail(
        subject="Account verification",
        message=f"Follow the link to activate your account: {full_link}",
        from_email=config("EMAIL_HOST"),
        recipient_list=[email]
    )
    
@app.task
def send_recovery_code(email: str, verify_code: str, secret: str) -> None:
    full_link = f"http://{config('SERVER_IP')}/api/v1/user/recover/{verify_code}/"
    
    send_mail(
        subject="Account reset",
        message=f"Follow the link to reset your account credentials: {full_link}"
        + f"\nHere is your secret: {secret}\nDo not share with anyone.",
        from_email=config("EMAIL_HOST"),
        recipient_list=[email]
    )