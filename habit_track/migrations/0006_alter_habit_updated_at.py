# Generated by Django 4.2.4 on 2023-08-27 01:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habit_track', '0005_habitcheck'),
    ]

    operations = [
        migrations.AlterField(
            model_name='habit',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 27, 8, 33, 52, 497360)),
        ),
    ]
