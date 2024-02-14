from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from stats.models import DeploymentDownload
from real_time_data.models import SBDData
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
            Notification.objects.create(for_user_id=1, from_user=instance.user, type='deployment_download', content={'deployment_id': instance.deployment.id, 'deployment_slug': instance.deployment.slug, 'deployment_name': instance.deployment.name, 'from_user_details': {'first_name': instance.user.first_name, 'last_name': instance.user.last_name, 'avatar': instance.user.userprofile.get_avatar()}})


@ receiver(post_save, sender=SBDData)
def admin_sbd_downloaded_notification(sender, instance, created, **kwargs):
    """
    Send a notification to admins when an SBD message entry is received. For now, 
    this will be when any entry is made. Later we should update it to only 
    activate when an SBD is received from Pub Sub
    """
    if created: 
        Notification.objects.create(for_user_id=1, from_user_id=1, type='sbd_message_received', content={'deployment_id': instance.deployment.id, 'deployment_slug': instance.deployment.slug, 'deployment_name': instance.deployment.name, 'sbd_filename': instance.sbd_filename})
