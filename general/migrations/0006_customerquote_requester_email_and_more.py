# Generated by Django 4.2 on 2023-07-19 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0005_customerquote'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerquote',
            name='requester_email',
            field=models.CharField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='customerquote',
            name='requester_name',
            field=models.CharField(blank=True, null=True),
        ),
    ]
