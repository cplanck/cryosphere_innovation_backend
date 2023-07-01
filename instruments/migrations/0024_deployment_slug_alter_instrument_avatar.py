# Generated by Django 4.2 on 2023-07-01 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instruments', '0023_alter_instrument_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='deployment',
            name='slug',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='instrument',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='users-media/instruments/avatars'),
        ),
    ]