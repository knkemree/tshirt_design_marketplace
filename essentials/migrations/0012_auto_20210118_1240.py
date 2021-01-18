# Generated by Django 3.1.3 on 2021-01-18 18:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('essentials', '0011_auto_20210118_1207'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='technique',
            name='technique',
        ),
        migrations.RemoveField(
            model_name='color',
            name='color_tag',
        ),
        migrations.RemoveField(
            model_name='product',
            name='technique',
        ),
        migrations.AlterField(
            model_name='color',
            name='color_code',
            field=models.CharField(blank=True, help_text='Start with #. Texture has priorty on color code. either color code or texture will be color option to customers', max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='color',
            name='texture',
            field=models.ImageField(blank=True, help_text='Start with #. Texture has priorty on color code. either color code or texture will be color option to customers', null=True, upload_to='textures/'),
        ),
        migrations.AlterField(
            model_name='design',
            name='email',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='designs', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='design',
            name='variant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='designs', to='essentials.variant'),
        ),
        migrations.AlterField(
            model_name='method',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='methods', to='essentials.product'),
        ),
        migrations.AlterField(
            model_name='method',
            name='technique',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='essentials.techniquebase'),
        ),
        migrations.AlterField(
            model_name='placement',
            name='placement',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='placements', to='essentials.placementbase'),
        ),
        migrations.AlterField(
            model_name='placement',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='placements', to='essentials.product'),
        ),
        migrations.DeleteModel(
            name='Mockup',
        ),
        migrations.DeleteModel(
            name='Technique',
        ),
    ]