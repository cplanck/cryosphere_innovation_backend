from math import fabs

from django.contrib.auth.models import User
from django.db import models
from django.db.models import ImageField
from instruments.models import Deployment

class PinnedDeployment(models.Model):
    deployment = Deployment
    date_pinned = models.DateTimeField(auto_now_add=True, null=True)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    avatar = models.ImageField(
        upload_to='users/avatars', null=True, blank=True)
    google_avatar = models.CharField(blank=True, null=True)
    robot = models.CharField(default='Snickers', blank=True, null=True)
    social_login = models.BooleanField(null=True, blank=True)
    has_social_avatar = models.BooleanField(null=True, blank=True)
    beta_tester = models.BooleanField(null=True, blank=True, default=False)
    has_made_deployment = models.BooleanField(null=True, blank=True)
    has_made_instrument = models.BooleanField(null=True, blank=True)
    dashboard_deployments = models.ManyToManyField(
        Deployment, blank=True)
    dashboard_deployment_order = models.JSONField(null=True, blank=True)
    # pinned_deployments = models.ManyToManyField(PinnedDeployment, blank=True)

    def get_avatar(self):
        if(self.avatar):
            return self.avatar.url
        elif(self.google_avatar):
            return self.google_avatar
        else:
            return f'https://api.dicebear.com/6.x/identicon/png?scale=70&seed={self.robot}'