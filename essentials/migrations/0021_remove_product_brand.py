# Generated by Django 3.1.3 on 2021-02-04 15:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('essentials', '0020_product_brand'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='brand',
        ),
    ]