# Generated by Django 3.1.3 on 2021-02-23 19:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_auto_20210223_1346'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderitem',
            old_name='bundle2',
            new_name='bundle',
        ),
        migrations.RenameField(
            model_name='orderitem',
            old_name='is_digital_product2',
            new_name='is_digital_product',
        ),
    ]
