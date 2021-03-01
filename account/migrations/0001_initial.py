# Generated by Django 3.1.5 on 2021-03-01 19:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('first_name', models.CharField(max_length=30, verbose_name='First Name')),
                ('last_name', models.CharField(max_length=30, verbose_name='Last Name')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None)),
                ('admin', models.BooleanField(default=False)),
                ('staff', models.BooleanField(default=False)),
                ('seller', models.BooleanField(blank=True, default=False, null=True)),
                ('stripe_id', models.CharField(max_length=150)),
                ('is_active', models.BooleanField(default=True)),
                ('remember_me', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='last login')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'All Users',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(blank=True, max_length=50)),
                ('comment', models.CharField(blank=True, max_length=250)),
                ('rate', models.IntegerField(default=1)),
                ('ip', models.CharField(blank=True, max_length=20)),
                ('active', models.BooleanField(default=True)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=False)),
                ('email_confirmed', models.BooleanField(default=False)),
                ('credit', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='creator', to=settings.AUTH_USER_MODEL, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Credit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_by', models.CharField(choices=[('staff', 'Staff'), ('seller', 'Seller')], default='staff', max_length=10)),
                ('added_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('stripe_id', models.CharField(blank=True, max_length=150, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('email', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='credits', to='account.seller')),
            ],
        ),
    ]
