# Generated by Django 4.2 on 2024-02-20 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instruments', '0051_rename_placeholder_deploymentmedia_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='deploymentmedia',
            name='last_modified',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
