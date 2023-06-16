import uuid

from django.contrib.auth.models import User
from django.db import models
from django.db.models import ImageField

# from api.base_models import *


class DeploymentTags(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=7)

    def __str__(self):
        return self.name


# class SIMB3(Instrument):

#     """
#     Main SIMB3 instrument model. Inherites from the base instrument model
#     and adds SIMB3 specific requirements
#     """

#     imei = models.CharField(max_length=100, null=True)
#     owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
#     version = models.IntegerField(default=1, blank=True)
#     sensor_suite = models.IntegerField(default=1, blank=True)
#     transmission_interval = models.IntegerField(default=4, blank=True)
#     build_date = models.DateField(null=True, blank=True)
#     fetch_data = models.BooleanField(default=True)
#     decode = models.BooleanField(default=True)
#     post_to_database = models.BooleanField(default=True)


# class SIMB3Deployment(Deployment):

#     """
#     Main SIMB3 deployment model. In most cases, there should only be
#     one deployment instance for SIMB3.
#     """

#     instrument = models.ForeignKey(
#         SIMB3, on_delete=models.CASCADE, null=True)
#     tags = models.ManyToManyField(DeploymentTags, blank=True)
#     deployment_ice_thickness = models.FloatField(null=True, blank=True)
#     deployment_snow_thickness = models.FloatField(null=True, blank=True)
#     starting_row = models.IntegerField(default=0)
#     ending_row = models.IntegerField(default=None, blank=True, null=True)
#     mb_plot_parameters = models.CharField(
#         max_length=50, default='0.5,-0.5,0,0,-3,0', blank=True, null=True)


# Later on...
# class PublicInstrument(Instrument):
    # owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    # imei = models.CharField(max_length=100, null=True)
    # ....
