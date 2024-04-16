# Generated by Django 5.0.3 on 2024-04-11 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsaggregator', '0007_rename_byline_health_h_byline_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='source',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='health',
            name='h_source',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sports',
            name='s_source',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]