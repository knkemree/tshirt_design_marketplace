# Generated by Django 3.1.3 on 2021-02-23 19:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_auto_20210223_1349'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='bundle1',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='is_digital_product1',
        ),
    ]
