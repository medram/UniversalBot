# Generated by Django 3.0.5 on 2020-05-08 16:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('universalbot', '0011_server_created'),
    ]

    operations = [
        migrations.RenameField(
            model_name='proxy',
            old_name='proxy',
            new_name='ip',
        ),
    ]