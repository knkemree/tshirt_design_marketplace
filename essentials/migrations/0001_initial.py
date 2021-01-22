# Generated by Django 3.1.5 on 2021-01-22 03:48

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taggit', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
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
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='essentials.category')),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
                'unique_together': {('slug', 'title')},
            },
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.CharField(blank=True, help_text='e.g. black adult tshirts, black youth tshirts, black hoodies (this field only for admins and not visible to customers)', max_length=40, null=True)),
                ('name', models.CharField(help_text='e.g black (this field is visible to customers)', max_length=40)),
                ('color_code', models.CharField(blank=True, help_text='texture has priorty on color code. either color code or texture will be color option to customers', max_length=40, null=True)),
                ('texture', models.ImageField(blank=True, help_text='texture has priorty on color code. either color code or texture will be color option to customers', null=True, upload_to='textures/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Font',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='PlacementBase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, help_text="e.g. 'front' or 'back'", max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('slug', models.SlugField(unique=True)),
                ('variant_type', models.CharField(choices=[('None', 'None'), ('Size', 'Size'), ('Color', 'Color'), ('Size-Color', 'Size-Color')], default='None', max_length=10)),
                ('description', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True)),
                ('image', models.ImageField(upload_to='images/')),
                ('active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='essentials.category')),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('row_no', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['row_no'],
            },
        ),
        migrations.CreateModel(
            name='Variant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('cost', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('sale_price', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('color', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='essentials.color')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variants', to='essentials.product')),
                ('size', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='essentials.size')),
            ],
            options={
                'ordering': ['color'],
            },
        ),
        migrations.CreateModel(
            name='TechniqueBase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('fonts', models.ManyToManyField(blank=True, null=True, related_name='technique_bases', to='essentials.Font')),
            ],
        ),
        migrations.CreateModel(
            name='Technique',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('technique', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='essentials.techniquebase')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='technique',
            field=models.ManyToManyField(blank=True, null=True, related_name='products', to='essentials.Technique'),
        ),
        migrations.CreateModel(
            name='Placement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('row_no', models.IntegerField(blank=True, default=0, null=True)),
                ('price', models.DecimalField(decimal_places=2, default=0, help_text='price for this placement', max_digits=12)),
                ('image', models.ImageField(upload_to='background_transparent_images/')),
                ('width', models.CharField(blank=True, max_length=10, null=True)),
                ('height', models.CharField(blank=True, max_length=10, null=True)),
                ('top', models.CharField(blank=True, max_length=10, null=True)),
                ('left', models.CharField(blank=True, max_length=10, null=True)),
                ('placement', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='placements', to='essentials.placementbase')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='placements', to='essentials.product')),
            ],
            options={
                'ordering': ['row_no'],
            },
        ),
        migrations.CreateModel(
            name='Mockup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, upload_to='images/')),
                ('active', models.BooleanField(default=True)),
                ('item_color', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mockups', to='essentials.color')),
            ],
            options={
                'ordering': ('item_color',),
            },
        ),
        migrations.CreateModel(
            name='Method',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, default=0, help_text='price for this printing method', max_digits=12)),
                ('row_no', models.IntegerField(blank=True, default=0, null=True)),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='methods', to='essentials.product')),
                ('technique', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='essentials.techniquebase')),
            ],
            options={
                'ordering': ['row_no'],
            },
        ),
        migrations.CreateModel(
            name='Design',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('end_product_img', models.ImageField(upload_to='end_product_imgs/')),
                ('image', models.ImageField(upload_to='designs/')),
                ('email', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='designs', to=settings.AUTH_USER_MODEL)),
                ('variant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='designs', to='essentials.variant')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='product',
            unique_together={('slug', 'title')},
        ),
    ]
