# Generated by Django 3.1.3 on 2020-11-30 23:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_buyer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buyer',
            name='buyer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shopper', to=settings.AUTH_USER_MODEL, unique=True),
        ),
    ]
