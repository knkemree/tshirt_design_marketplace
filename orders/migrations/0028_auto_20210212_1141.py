# Generated by Django 3.1.5 on 2021-02-12 17:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_credit'),
        ('orders', '0027_auto_20210205_1148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='ordered_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='account.seller'),
        ),
    ]
