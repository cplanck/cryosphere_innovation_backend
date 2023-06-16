# Generated by Django 4.2 on 2023-05-21 20:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('instruments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='instrument',
            name='imei',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='instrument',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
