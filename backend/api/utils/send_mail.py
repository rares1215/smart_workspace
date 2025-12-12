from django.core.mail import send_mail
from django.conf import settings

def send_verification_email(email: str, code: str):
    subject = "Verify your account"
    message = f"""
Hello, Thank you for registering to smart_workspace.com, You recived a verification code to validate your account.

Your verification code is:

{code}

This code will expire in 10 minutes.

If you did not create this account, please ignore this email.
"""

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )
