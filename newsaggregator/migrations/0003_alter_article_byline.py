# Generated by Django 5.0.3 on 2024-03-26 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsaggregator', '0002_delete_source_remove_article_source_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='byline',
            field=models.TextField(default='', max_length=255),
        ),
    ]
