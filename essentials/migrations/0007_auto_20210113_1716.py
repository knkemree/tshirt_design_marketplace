# Generated by Django 3.1.3 on 2021-01-13 23:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('essentials', '0006_placement_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='Font',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='techniquebase',
            name='fonts',
            field=models.ManyToManyField(blank=True, null=True, related_name='technique_bases', to='essentials.Font'),
        ),
    ]