# Generated by Django 3.1.3 on 2021-01-26 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('essentials', '0014_auto_20210126_1337'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClrBase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('color_code', models.CharField(blank=True, help_text='texture has priorty on color code. either color code or texture will be color option to customers', max_length=40, null=True)),
                ('texture', models.ImageField(blank=True, help_text='texture has priorty on color code. either color code or texture will be color option to customers', null=True, upload_to='textures/')),
                ('row_no', models.IntegerField(blank=True, default=0, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Clr -Test',
                'verbose_name_plural': 'Clrs -Test',
                'ordering': ['row_no'],
            },
        ),
        migrations.CreateModel(
            name='SzBase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('row_no', models.IntegerField(blank=True, default=0, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Sz -Test',
                'verbose_name_plural': 'Szs -Test',
                'ordering': ['row_no'],
            },
        ),
    ]