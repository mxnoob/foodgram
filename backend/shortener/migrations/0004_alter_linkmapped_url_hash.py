# Generated by Django 4.2.11 on 2024-04-29 23:13

from django.db import migrations, models
import shortener.models


class Migration(migrations.Migration):
    dependencies = [
        ('shortener', '0003_alter_linkmapped_original_url_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='linkmapped',
            name='url_hash',
            field=models.CharField(
                default=shortener.models.generate_hash, max_length=15
            ),
        ),
    ]
