# Generated by Django 3.1.3 on 2021-02-27 17:32

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('essentials', '0032_auto_20210227_1131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='design',
            name='uuid3',
            field=models.UUIDField(default=uuid.uuid4, null=True),
        ),
    ]
