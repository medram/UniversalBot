# Generated by Django 3.0.5 on 2020-05-08 15:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('universalbot', '0007_auto_20200507_1627'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='proxy',
            field=models.ForeignKey(blank=True, limit_choices_to={'active': True}, null=True, on_delete=django.db.models.deletion.SET_NULL, to='universalbot.Proxy'),
        ),
    ]