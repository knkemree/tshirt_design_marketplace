# Generated by Django 3.1.3 on 2021-01-28 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_auto_20210124_0210'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='attachment',
            field=models.FileField(blank=True, help_text='Check here for gift card', null=True, upload_to='uploads/'),
        ),
    ]
