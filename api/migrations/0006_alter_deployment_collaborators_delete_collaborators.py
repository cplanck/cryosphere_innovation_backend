# Generated by Django 4.2 on 2023-04-29 18:54

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0005_remove_deployment_instrument_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deployment',
            name='collaborators',
            field=models.ManyToManyField(related_name='collaborators', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Collaborators',
        ),
    ]
