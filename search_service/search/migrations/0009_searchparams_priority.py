# Generated by Django 5.1.5 on 2025-02-01 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0008_rename_search_enabled_searchparams_enabled_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='searchparams',
            name='priority',
            field=models.IntegerField(default=0),
        ),
    ]
