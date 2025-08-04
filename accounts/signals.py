from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
from django.core.mail import send_mail

@receiver(user_logged_in)
def send_login_email(sender, request, user, **kwargs):
    subject = 'Welcome back to SellHub!'
    message = f'Hello {user.email}, you have successfully logged in.'
    from_email = 'no-reply@sellhub.com'
    recipient_list = [user.email]

    send_mail(subject, message, from_email, recipient_list)
