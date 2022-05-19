from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import mail_managers
from .models import Post



@receiver(post_save, sender=Post)
def notify_subscriber(sender, instance, created, **kwargs):
    if created:
        print(type(instance))


