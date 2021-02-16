# Generated by Django 3.1.3 on 2021-02-16 01:21

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('mockups', '0002_remove_mockup_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='mockup',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
