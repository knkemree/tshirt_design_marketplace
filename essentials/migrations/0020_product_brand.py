# Generated by Django 3.1.3 on 2021-02-03 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('essentials', '0019_merge_20210203_1628'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='brand',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
