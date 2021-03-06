# Generated by Django 3.1.3 on 2021-03-04 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('essentials', '0004_auto_20210304_1417'),
    ]

    operations = [
        migrations.AlterField(
            model_name='placement',
            name='height',
            field=models.CharField(blank=True, default='30', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='placement',
            name='left',
            field=models.CharField(blank=True, default='30%', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='placement',
            name='top',
            field=models.CharField(blank=True, default='30%', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='placement',
            name='width',
            field=models.CharField(blank=True, default='30', max_length=10, null=True),
        ),
    ]
