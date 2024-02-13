# Generated by Django 4.2 on 2024-02-13 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0004_notification_date_added_notification_last_modified'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='expiration',
        ),
        migrations.AddField(
            model_name='notification',
            name='deleted',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
