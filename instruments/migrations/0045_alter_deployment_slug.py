# Generated by Django 4.2 on 2024-02-13 22:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instruments', '0044_alter_instrument_sensors'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deployment',
            name='slug',
            field=models.CharField(blank=True, max_length=500, null=True, unique=True),
        ),
    ]
