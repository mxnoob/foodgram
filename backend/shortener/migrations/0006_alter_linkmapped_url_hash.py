# Generated by Django 4.2.11 on 2024-05-01 14:07

from django.db import migrations, models
import shortener.models


class Migration(migrations.Migration):
    dependencies = [
        ("shortener", "0005_alter_linkmapped_options"),
    ]

    operations = [
        migrations.AlterField(
            model_name="linkmapped",
            name="url_hash",
            field=models.CharField(
                default=shortener.models.generate_hash, max_length=15, unique=True
            ),
        ),
    ]
