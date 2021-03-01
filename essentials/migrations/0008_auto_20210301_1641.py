# Generated by Django 3.1.5 on 2021-03-01 22:41

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('essentials', '0007_auto_20210301_1546'),
    ]

    operations = [
        migrations.AlterField(
            model_name='design',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, null=True),
        ),
        migrations.AlterField(
            model_name='variant',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, null=True),
        ),
    ]
