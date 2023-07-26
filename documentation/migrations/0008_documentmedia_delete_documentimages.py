# Generated by Django 4.2 on 2023-07-26 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documentation', '0007_remove_documentimages_documentation_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.ImageField(blank=True, null=True, upload_to='documentation/media')),
                ('type', models.CharField(blank=True, null=True)),
                ('size', models.CharField(blank=True, null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='DocumentImages',
        ),
    ]
