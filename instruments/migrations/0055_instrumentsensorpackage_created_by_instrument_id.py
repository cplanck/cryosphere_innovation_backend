# Generated by Django 4.2 on 2024-03-11 03:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instruments', '0054_alter_deployment_rows_from_end'),
    ]

    operations = [
        migrations.AddField(
            model_name='instrumentsensorpackage',
            name='created_by_instrument_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
