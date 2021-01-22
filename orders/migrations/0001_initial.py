# Generated by Django 3.1.5 on 2021-01-22 03:38

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('coupons', '__first__'),
        ('account', '0002_auto_20210121_2138'),
        ('essentials', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipient', models.CharField(blank=True, max_length=50, null=True)),
                ('shipping_label', models.FileField(blank=True, null=True, upload_to='uploads/')),
                ('total', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('note', models.CharField(blank=True, max_length=1000, null=True)),
                ('discount', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('shipping_fee', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('profit', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('paid', models.BooleanField(default=False)),
                ('fulfillment', models.BooleanField(default=False)),
                ('stripe_id', models.CharField(blank=True, max_length=150)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('coupon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='coupons.coupon')),
                ('ordered_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.seller')),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('technique', models.CharField(blank=True, max_length=100, null=True)),
                ('end_product_img', models.ImageField(blank=True, null=True, upload_to='end_product_imgs/')),
                ('image', models.ImageField(blank=True, null=True, upload_to='designs/')),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('cost', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('json_data', models.JSONField(blank=True, null=True)),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='items', to='orders.order')),
                ('variant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_items', to='essentials.variant')),
            ],
        ),
    ]
