# Generated by Django 4.2.7 on 2023-11-16 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='source',
            name='url',
            field=models.URLField(max_length=255, null=True),
        ),
    ]
