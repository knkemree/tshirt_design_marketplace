# Generated by Django 3.1.5 on 2021-03-01 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('essentials', '0004_auto_20210301_1543'),
    ]

    operations = [
        migrations.AddField(
            model_name='design',
            name='uuid5',
            field=models.UUIDField(null=True),
        ),
        migrations.AddField(
            model_name='variant',
            name='uuid5',
            field=models.UUIDField(null=True),
        ),
    ]
