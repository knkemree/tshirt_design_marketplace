# Generated by Django 3.1.3 on 2020-11-30 18:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_auto_20201130_1200'),
    ]

    operations = [
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('email_confirmed', models.BooleanField(default=False)),
                ('seller', models.ForeignKey(help_text='Customer has already seller account', on_delete=django.db.models.deletion.CASCADE, related_name='creator', to=settings.AUTH_USER_MODEL, unique=True)),
            ],
        ),
    ]
