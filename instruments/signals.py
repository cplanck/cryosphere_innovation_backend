from data.dynamodb import *
from data.mongodb import *
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Deployment, Instrument


@receiver(post_save, sender=Deployment)
def create_mongo_db_collection_for_deployment(sender, instance, created, **kwargs):
    """
    Automatically create a new MongoDB collection when a new deployment is added.
    """
    print(instance)
    if created and not mongo_collection_exists(str(instance.data_uuid)):
        create_mongodb_collection(str(instance.data_uuid), 'time_stamp')


@receiver(post_delete, sender=Deployment)
def delete_mongo_db_collection_for_deployment(sender, instance, **kwargs):
    """
    Automatically delete a MongoDB collection when a deployment is deleted
    """
    delete_mongodb_collection(str(instance.data_uuid))
