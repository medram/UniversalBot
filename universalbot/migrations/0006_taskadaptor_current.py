# Generated by Django 3.0.5 on 2020-05-06 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('universalbot', '0005_auto_20200506_1506'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskadaptor',
            name='current',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
