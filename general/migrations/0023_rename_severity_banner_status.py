# Generated by Django 4.2 on 2024-02-12 19:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0022_banner_active'),
    ]

    operations = [
        migrations.RenameField(
            model_name='banner',
            old_name='severity',
            new_name='status',
        ),
    ]
