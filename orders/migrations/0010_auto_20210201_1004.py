# Generated by Django 3.1.3 on 2021-02-01 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0009_order_attachment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='fulfillment',
            field=models.BooleanField(default=False, help_text='Customer will be notified via email if marked.'),
        ),
    ]