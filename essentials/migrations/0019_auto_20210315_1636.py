# Generated by Django 3.1.3 on 2021-03-15 21:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('essentials', '0018_auto_20210309_1144'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='variant',
            options={'ordering': ['size', 'color']},
        ),
    ]