# Generated by Django 4.2 on 2023-05-29 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0003_rename_articles_article'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='internal',
            field=models.BooleanField(default=False),
        ),
    ]
