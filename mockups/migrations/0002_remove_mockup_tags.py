# Generated by Django 3.1.3 on 2021-02-12 23:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mockups', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mockup',
            name='tags',
        ),
    ]
