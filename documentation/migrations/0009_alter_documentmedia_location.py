# Generated by Django 4.2 on 2023-07-26 14:20

from django.db import migrations, models
import documentation.models


class Migration(migrations.Migration):

    dependencies = [
        ('documentation', '0008_documentmedia_delete_documentimages'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentmedia',
            name='location',
            field=models.FileField(blank=True, null=True, upload_to=documentation.models.custom_filename),
        ),
    ]
