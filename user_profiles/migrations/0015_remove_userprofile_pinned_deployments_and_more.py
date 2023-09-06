# Generated by Django 4.2 on 2023-09-05 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profiles', '0014_pinneddeployment_userprofile_pinned_deployments'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='pinned_deployments',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='dashboard_deployment_order',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
