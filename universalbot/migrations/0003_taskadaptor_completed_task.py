# Generated by Django 3.0.5 on 2020-04-18 16:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('background_task', '0002_auto_20170927_1109'),
        ('universalbot', '0002_auto_20200418_1722'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskadaptor',
            name='completed_task',
            field=models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='background_task.CompletedTask'),
        ),
    ]
