# Generated by Django 4.2.19 on 2025-02-13 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kontrak', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kontrak',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
