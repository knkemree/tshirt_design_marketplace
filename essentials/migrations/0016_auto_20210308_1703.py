# Generated by Django 3.1.3 on 2021-03-08 23:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('essentials', '0015_auto_20210308_1701'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='variant',
            options={'ordering': ['color', 'size']},
        ),
    ]
