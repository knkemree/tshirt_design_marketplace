# Generated by Django 3.1.3 on 2021-03-04 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('essentials', '0009_auto_20210304_1457'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='title',
            field=models.CharField(max_length=150, null=True),
        ),
    ]
