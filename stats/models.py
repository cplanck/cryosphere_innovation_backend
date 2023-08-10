from django.db import models
from instruments.models import Deployment
from django.contrib.auth.models import User

class DeploymentDownload(models.Model):
    deployment = models.ForeignKey(Deployment, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True, null=True)