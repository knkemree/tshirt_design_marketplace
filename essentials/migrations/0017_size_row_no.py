# Generated by Django 3.1.3 on 2020-12-31 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('essentials', '0016_auto_20201231_1535'),
    ]

    operations = [
        migrations.AddField(
            model_name='size',
            name='row_no',
            field=models.IntegerField(default=0),
        ),
    ]