# Generated by Django 4.2 on 2023-08-04 23:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_profiles', '0011_userprofile_can_add_models'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='can_add_models',
            new_name='beta_tester',
        ),
    ]
