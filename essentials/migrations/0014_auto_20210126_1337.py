# Generated by Django 3.1.3 on 2021-01-26 19:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('essentials', '0013_auto_20210126_1331'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ClrBase',
        ),
        migrations.DeleteModel(
            name='SzBase',
        ),
    ]