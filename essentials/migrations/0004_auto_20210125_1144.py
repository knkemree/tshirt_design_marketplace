# Generated by Django 3.1.3 on 2021-01-25 17:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('essentials', '0003_auto_20210125_1141'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='method',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='essentials.method'),
        ),
        migrations.AddField(
            model_name='product',
            name='placement',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='essentials.placement'),
        ),
        migrations.DeleteModel(
            name='Technique',
        ),
    ]
