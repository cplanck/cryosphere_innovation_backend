# Generated by Django 4.2 on 2024-03-12 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instruments', '0055_instrumentsensorpackage_created_by_instrument_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='instrument',
            name='build_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
