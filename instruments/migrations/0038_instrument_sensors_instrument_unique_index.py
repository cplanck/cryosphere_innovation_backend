# Generated by Django 4.2 on 2023-08-13 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instruments', '0037_alter_instrument_avatar_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='instrument',
            name='sensors',
            field=models.JSONField(blank=True, default={}, null=True),
        ),
        migrations.AddField(
            model_name='instrument',
            name='unique_index',
            field=models.CharField(blank=True, null=True),
        ),
    ]
