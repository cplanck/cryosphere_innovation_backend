from django.core.mail import send_mail
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .models import *


def send_email(instance):
    html_message = render_to_string(
        'general/quote_request_email.html', {'instance': instance})
    plain_message = strip_tags(html_message)
    send_mail(
        subject="Your SIMB3 quote is on the way 🚀",
        message=plain_message,
        from_email='support@cryosphereinnovation.com',
        recipient_list=[instance.details['requester_email'],
                        'cjp@cryosphereinnovation.com'],
        html_message=html_message,
        fail_silently=False,
    )


def send_client_contact_us_form_email(instance):
    html_message = render_to_string(
        'general/contact_us_form_email.html', {'instance': instance})
    plain_message = strip_tags(html_message)
    send_mail(
        subject="We received your submission 🎉",
        message=plain_message,
        from_email='support@cryosphereinnovation.com',
        recipient_list=[instance.form_results['email']],
        html_message=html_message,
        fail_silently=False,
    )


def send_admin_contact_us_form_email(instance):
    html_message = render_to_string(
        'general/contact_us_form_email_admin.html', {'instance': instance})
    plain_message = strip_tags(html_message)
    send_mail(
        subject="We received your submission 🎉",
        message=plain_message,
        from_email='support@cryosphereinnovation.com',
        recipient_list=['cjp@cryosphereinnovation.com'],
        html_message=html_message,
        fail_silently=False,
    )


@ receiver(post_save, sender=CustomerQuote)
def send_quote_submission_email(sender, instance, created, **kwargs):
    """
    Send user a confirmation email that we recieved their SIMB3 quote
    """
    if created:
        send_email(instance)


@ receiver(post_save, sender=ContactUs)
def send_contact_use_submission_email(sender, instance, created, **kwargs):
    """
    Send user a confirmation email that we recieved their contact form
    """
    if created:
        send_client_contact_us_form_email(instance)
        send_admin_contact_us_form_email(instance)
