# Generated by Django 3.1.3 on 2021-01-25 17:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('essentials', '0005_auto_20210125_1153'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='placementbase',
            options={'verbose_name': 'Placement', 'verbose_name_plural': 'Placements'},
        ),
        migrations.AlterModelOptions(
            name='techniquebase',
            options={'verbose_name': 'Technique', 'verbose_name_plural': 'Techniques'},
        ),
    ]