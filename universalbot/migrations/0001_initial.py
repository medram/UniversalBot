# Generated by Django 3.0.5 on 2020-04-18 12:20

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('background_task', '0002_auto_20170927_1109'),
    ]

    operations = [
        migrations.CreateModel(
            name='List',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True)),
                ('actions', multiselectfield.db.fields.MultiSelectField(choices=[(1, 'Inbox, add all to archive'), (2, 'Inbox, mark all as read'), (3, 'Spam, report all to inbox')], max_length=256)),
                ('file', models.FileField(blank=True, null=True, upload_to='profiles_lists/%Y/%m/', validators=[django.core.validators.FileExtensionValidator(['csv'])], verbose_name='Load profiles from a csv file')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=64, unique=True)),
                ('password', models.CharField(max_length=64)),
                ('status', models.BooleanField(default=False)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Proxy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('proxy', models.GenericIPAddressField()),
                ('port', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(65535), django.core.validators.MinValueValidator(0)])),
                ('active', models.BooleanField(default=True, help_text='Active means that the server proxy is up and running and is ready to use.')),
            ],
            options={
                'verbose_name_plural': 'Proxies',
                'db_table': 'proxies',
            },
        ),
        migrations.CreateModel(
            name='TaskAdaptor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('run_at', models.DateTimeField(db_index=True)),
                ('repeat', models.BigIntegerField(choices=[(3600, 'hourly'), (86400, 'daily'), (604800, 'weekly'), (1209600, 'every 2 weeks'), (2419200, 'every 4 weeks'), (0, 'never')], default=0)),
                ('repeat_until', models.DateTimeField(blank=True, null=True)),
                ('task_name', models.CharField(max_length=255, null=True, unique=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('lists', models.ManyToManyField(to='universalbot.List')),
                ('task', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='background_task.Task')),
            ],
            options={
                'verbose_name': 'Task',
                'verbose_name_plural': 'Tasks',
                'db_table': 'task_adaptors',
            },
        ),
        migrations.AddField(
            model_name='list',
            name='profiles',
            field=models.ManyToManyField(blank=True, to='universalbot.Profile'),
        ),
    ]
