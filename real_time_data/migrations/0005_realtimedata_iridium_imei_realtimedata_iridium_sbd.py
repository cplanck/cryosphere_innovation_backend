# Generated by Django 4.2 on 2023-08-07 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('real_time_data', '0004_realtimedata_updated'),
    ]

    operations = [
        migrations.AddField(
            model_name='realtimedata',
            name='iridium_imei',
            field=models.CharField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='realtimedata',
            name='iridium_sbd',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
    ]