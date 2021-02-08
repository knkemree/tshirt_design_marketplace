# Generated by Django 3.1.3 on 2021-02-05 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0024_auto_20210205_1043'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='fulfillment',
        ),
        migrations.AddField(
            model_name='order',
            name='customer_notified',
            field=models.BooleanField(default=False, help_text='When marked the customer will be notified via email that the order has been fulfilled'),
        ),
    ]