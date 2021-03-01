# Generated by Django 3.1.3 on 2021-03-01 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('essentials', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='design',
            old_name='uuid',
            new_name='uuid1',
        ),
        migrations.RenameField(
            model_name='variant',
            old_name='uuid',
            new_name='uuid1',
        ),
        migrations.AddField(
            model_name='design',
            name='uuid2',
            field=models.UUIDField(null=True),
        ),
        migrations.AddField(
            model_name='variant',
            name='uuid2',
            field=models.UUIDField(null=True),
        ),
    ]
