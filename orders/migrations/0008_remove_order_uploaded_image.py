# Generated by Django 3.1.3 on 2020-12-28 21:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_order_uploaded_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='uploaded_image',
        ),
    ]
