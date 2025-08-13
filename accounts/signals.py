from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from .models import Profile

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        # Envoyer l'email de bienvenue
        send_welcome_email(instance)
    instance.profile.save()

def send_welcome_email(user):
    subject = 'Bienvenue sur SellHub !'
    html_message = render_to_string('accounts/welcome_email.html', {
        'user': user,
        'site_name': 'SellHub'
    })
    plain_message = strip_tags(html_message)
    
    try:
        send_mail(
            subject,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            html_message=html_message,
            fail_silently=False,
        )
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email de bienvenue: {e}")

@receiver(user_logged_in)
def send_login_email(sender, request, user, **kwargs):
    subject = 'Bienvenue de retour sur SellHub!'
    message = f'Bonjour {user.email}, vous vous êtes connecté avec succès.'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]

    send_mail(subject, message, from_email, recipient_list)
