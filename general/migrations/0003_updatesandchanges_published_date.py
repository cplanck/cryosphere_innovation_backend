# Generated by Django 4.2 on 2023-07-17 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0002_rename_heading_updatesandchanges_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='updatesandchanges',
            name='published_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
