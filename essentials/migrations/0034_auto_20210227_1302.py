# Generated by Django 3.1.3 on 2021-02-27 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('essentials', '0033_auto_20210227_1132'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='design',
            name='uuid3',
        ),
        migrations.AddField(
            model_name='design',
            name='uuid',
            field=models.UUIDField(null=True),
        ),
    ]
