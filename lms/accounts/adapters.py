from allauth.account.adapter import DefaultAccountAdapter
from django.contrib.sites.models import Site

current_site = Site.objects.get_current()
site_domain = current_site.domain

class CustomAccountAdapter(DefaultAccountAdapter):
        
    def get_email_confirmation_url(self, request, emailconfirmation):
        return f"http://{site_domain}/account/email-confirmation/{emailconfirmation.key}/"
    