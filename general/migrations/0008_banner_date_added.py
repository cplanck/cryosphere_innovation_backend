# Generated by Django 4.2 on 2023-07-20 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0007_banner_alter_customerquote_quote_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='banner',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
