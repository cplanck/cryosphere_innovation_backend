# Generated by Django 4.2 on 2024-02-10 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('real_time_data', '0013_rename_dowloading_realtimedata_downloading'),
    ]

    operations = [
        migrations.AddField(
            model_name='sbddata',
            name='gmail_message_id',
            field=models.CharField(blank=True, null=True, unique=True),
        ),
    ]
