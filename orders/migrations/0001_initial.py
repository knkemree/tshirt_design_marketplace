# Generated by Django 3.1.3 on 2021-03-01 21:30

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0002_auto_20210301_1528'),
        ('coupons', '0001_initial'),
        ('tasarimlar', '0006_auto_20210224_1142'),
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
                ('attachment', models.FileField(blank=True, help_text='Check here for gift card', null=True, upload_to='uploads/')),
                ('discount', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('shipping_fee', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('profit', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('paid', models.BooleanField(default=False)),
                ('customer_notified', models.BooleanField(default=False, help_text='When marked the customer will be notified via email that the order has been fulfilled')),
                ('status', models.CharField(choices=[('1', 'In Queue'), ('2', 'In Progress'), ('3', 'Fulfilled'), ('4', 'Cancelled')], default=1, max_length=10)),
                ('stripe_id', models.CharField(blank=True, max_length=150)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('coupon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='coupons.coupon')),
                ('ordered_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='account.seller')),
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
                ('placement', models.CharField(blank=True, max_length=100, null=True)),
                ('end_product_img', models.ImageField(blank=True, null=True, upload_to='end_product_imgs/')),
                ('image', models.ImageField(blank=True, null=True, upload_to='designs/')),
                ('product_type', models.CharField(blank=True, max_length=50, null=True)),
                ('is_digital_product2', models.BooleanField(default=False)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('cost', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('ready_to_ship', models.BooleanField(default=False)),
                ('log_entry', models.CharField(blank=True, max_length=200, null=True)),
                ('json_data', models.JSONField(blank=True, editable=False, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('bundle2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='items', to='tasarimlar.design')),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='orders.order')),
                ('variant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_items', to='essentials.variant')),
            ],
        ),
    ]
