# Generated by Django 4.2 on 2023-07-26 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0012_contactus'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactus',
            name='seen',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]