# Generated by Django 3.0.5 on 2020-05-08 16:09

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('universalbot', '0010_auto_20200508_1604'),
    ]

    operations = [
        migrations.AddField(
            model_name='server',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
