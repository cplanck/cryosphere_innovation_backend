# Generated by Django 4.2 on 2024-02-20 22:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instruments', '0052_deploymentmedia_last_modified'),
    ]

    operations = [
        migrations.AddField(
            model_name='deploymentmedia',
            name='name',
            field=models.CharField(blank=True, null=True),
        ),
    ]