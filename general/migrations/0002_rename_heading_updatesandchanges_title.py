# Generated by Django 4.2 on 2023-07-17 16:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='updatesandchanges',
            old_name='heading',
            new_name='title',
        ),
    ]