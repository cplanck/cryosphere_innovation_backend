# Generated by Django 4.2 on 2023-06-10 16:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_profiles', '0007_rename_watched_instruments_userprofile_watched_deployments'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='watched_deployments',
            new_name='dashboard_deployments',
        ),
    ]
