# Generated by Django 4.2 on 2023-07-25 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documentation', '0004_rename_documentation_document_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='type',
            field=models.CharField(choices=[('Doc', 'Doc'), ('Article', 'Article')], default='Doc', max_length=30),
        ),
    ]
