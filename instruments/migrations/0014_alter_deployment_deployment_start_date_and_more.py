# Generated by Django 4.2 on 2023-05-21 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instruments', '0013_instrument_instrument_type_instrument_internal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deployment',
            name='deployment_start_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='deployment',
            name='name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='deployment',
            name='private',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
        migrations.AlterField(
            model_name='deployment',
            name='starred',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='deployment',
            name='status',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]