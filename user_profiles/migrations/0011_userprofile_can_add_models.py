# Generated by Django 4.2 on 2023-08-04 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profiles', '0010_userprofile_robot'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='can_add_models',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
