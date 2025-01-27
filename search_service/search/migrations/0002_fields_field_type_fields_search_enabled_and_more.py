# Generated by Django 5.1.5 on 2025-01-26 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fields',
            name='field_type',
            field=models.CharField(default=None, max_length=32),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='fields',
            name='search_enabled',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='fields',
            name='search_weight',
            field=models.FloatField(default=1),
        ),
    ]
