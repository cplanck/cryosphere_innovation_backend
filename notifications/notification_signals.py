from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from stats.models import DeploymentDownload
from .models import Notification
from datetime import datetime

@ receiver(post_save, sender=DeploymentDownload)
def admin_deployment_download_notification(sender, instance, created, **kwargs):
    """
    Send an instrument owner a notification when someone downloads data from 
    one of their instruments
    """
    if created:
         # Don't sent notifications to Cameron if Cameron downloaded
         if not instance.user.id == 1:
            Notification.objects.create(for_user_id=1, from_user=instance.user, type='deployment_download', content={'deployment_id': instance.deployment.id, 'deployment_name': instance.deployment.name, 'from_user_details': {'first_name': instance.user.first_name, 'last_name': instance.user.last_name, 'avatar': instance.user.userprofile.get_avatar()}})



