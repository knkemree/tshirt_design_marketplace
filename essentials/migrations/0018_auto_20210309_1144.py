# Generated by Django 3.1.3 on 2021-03-09 17:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('essentials', '0017_auto_20210308_1704'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='variant',
            options={'ordering': ['color', 'size__row_no']},
        ),
    ]