# Generated by Django 3.1.3 on 2020-11-28 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_buyer_seller'),
    ]

    operations = [
        migrations.AddField(
            model_name='seller',
            name='email_confirmed',
            field=models.BooleanField(default=False),
        ),
    ]
