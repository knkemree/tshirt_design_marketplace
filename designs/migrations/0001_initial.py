# Generated by Django 3.1.5 on 2021-02-19 23:51

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Design',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=40, null=True)),
                ('slug', models.SlugField(unique=True)),
                ('digital_product', models.FileField(help_text='Customer will download this file upon succesfull payment', null=True, upload_to='digital_products/')),
                ('price', models.DecimalField(decimal_places=2, help_text='price for this digital product', max_digits=12, null=True)),
                ('cost', models.DecimalField(decimal_places=2, help_text='cost for this digital product', max_digits=12, null=True)),
                ('sales', models.IntegerField(default=0)),
                ('views', models.PositiveIntegerField(default=0)),
                ('active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['created_at', 'updated_at'],
            },
        ),
        migrations.CreateModel(
            name='DesignImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(null=True, upload_to='designs/%Y/%m/%d')),
                ('row_no', models.IntegerField(default=0)),
                ('active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('design', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='design_images', to='designs.design')),
            ],
            options={
                'ordering': ['row_no'],
            },
        ),
        migrations.CreateModel(
            name='Design_Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('slug', models.SlugField(unique=True)),
                ('description', models.TextField(max_length=255)),
                ('image', models.ImageField(blank=True, upload_to='images/')),
                ('active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='designs.design_category')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
                'unique_together': {('slug', 'title')},
            },
        ),
        migrations.AddField(
            model_name='design',
            name='categories',
            field=models.ManyToManyField(null=True, related_name='design_categories', to='designs.Design_Category'),
        ),
        migrations.AlterUniqueTogether(
            name='design',
            unique_together={('slug', 'title')},
        ),
    ]
