# Generated by Django 4.2.11 on 2024-04-29 21:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('shortener', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='linkmapped',
            name='url_hash',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]
