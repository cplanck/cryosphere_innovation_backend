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


# @receiver(user_signed_up)
# def create_user_profile(sender, request, sociallogin, **kwargs):
#     user = sociallogin.user
#     social_account = sociallogin.account

#     # Check if the user already has a UserProfile. This should always be true.
#     try:
#         user_profile = UserProfile.objects.get(user=user)
#     except UserProfile.DoesNotExist:
#         user_profile = None

#     # # Create a new UserProfile if necessary
#     # if not user_profile:
#     #     user_profile = UserProfile.objects.create(user=user)

#     # Update the social login flag on the UserProfile
#     user_profile.social_login = True if social_account.provider in [
#         'google'] else False

#     if social_account.provider == 'google':
#         extra_data = social_account.extra_data
#         if 'name' in extra_data:
#             user_profile.full_name = extra_data['name']
#         if 'picture' in extra_data:
#             user_profile.has_social_avatar = True

#     user_profile.save()
