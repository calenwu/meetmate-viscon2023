# Generated by Django 4.2.6 on 2023-10-20 20:13

import core.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='id',
            field=models.CharField(default=core.utils.generate_long_id, editable=False, max_length=64, primary_key=True, serialize=False),
        ),
    ]
