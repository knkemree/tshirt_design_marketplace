# Generated by Django 3.1.3 on 2020-12-31 23:21

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('essentials', '0022_auto_20201231_1615'),
    ]

    operations = [
        migrations.AddField(
            model_name='color',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='color',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
