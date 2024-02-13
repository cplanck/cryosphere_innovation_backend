# from allauth.account.signals import user_signed_up
# from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from user_profiles.models import UserProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance, full_name='', social_login=False,
                                   has_social_avatar=False, has_made_deployment=False, has_made_instrument=False)