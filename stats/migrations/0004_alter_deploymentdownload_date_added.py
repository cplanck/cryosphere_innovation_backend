# Generated by Django 4.2 on 2024-02-19 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0003_alter_deploymentdownload_date_added_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deploymentdownload',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]