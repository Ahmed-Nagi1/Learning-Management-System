from allauth.account.signals import email_confirmed
from django.dispatch import receiver
from allauth.account.models import EmailAddress

@receiver(email_confirmed)
def set_primary_email(sender, request, email_address, **kwargs):
    user = email_address.user
    EmailAddress.objects.filter(user=user).update(primary=False)
    email_address.primary = True
    email_address.save()
