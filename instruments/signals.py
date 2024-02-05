from data.dynamodb import *
from data.mongodb import *
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Deployment, Instrument
import json


@receiver(post_save, sender=Deployment)
def create_mongo_db_collection_for_deployment(sender, instance, created, **kwargs):
    """
    Automatically create a new MongoDB collection when a new deployment is added.
    """
    if created and not mongo_collection_exists(str(instance.data_uuid)):

        try:
            unique_index = instance.instrument.sensor_package.time_stamp_field['databaseName']
            instance.unique_index = unique_index
            instance.save()
            create_mongodb_collection(str(instance.data_uuid), unique_index)
        except Exception as e:
            create_mongodb_collection(str(instance.data_uuid))

        # create_mongodb_collection(str(instance.data_uuid), instance.instrument.unique_index)
        # create_mongodb_collection(str(instance.data_uuid), unique_index)

        # Save the unique index from the instrument to the deployment



@receiver(post_delete, sender=Deployment)
def delete_mongo_db_collection_for_deployment(sender, instance, **kwargs):
    """
    Automatically delete a MongoDB collection when a deployment is deleted
    """
    delete_mongodb_collection(str(instance.data_uuid))
