# Generated by Django 4.2 on 2023-08-07 20:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('real_time_data', '0002_rename_realtimedecoding_realtimedata'),
    ]

    operations = [
        migrations.CreateModel(
            name='DecodeScript',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, null=True)),
                ('script', models.TextField(blank=True, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_modified', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.AlterModelOptions(
            name='realtimedata',
            options={'verbose_name': 'Real-Time Data', 'verbose_name_plural': 'Real-Time Data'},
        ),
        migrations.RenameField(
            model_name='realtimedata',
            old_name='decode_script_name',
            new_name='error',
        ),
        migrations.AddField(
            model_name='realtimedata',
            name='decode_script',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='real_time_data.decodescript'),
        ),
    ]