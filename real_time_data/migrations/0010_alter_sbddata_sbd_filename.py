# Generated by Django 4.2 on 2024-02-09 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('real_time_data', '0009_sbddata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sbddata',
            name='sbd_filename',
            field=models.CharField(blank=True, null=True, unique=True),
        ),
    ]