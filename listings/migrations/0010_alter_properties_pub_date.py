# Generated by Django 4.0.3 on 2024-02-29 06:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0009_alter_properties_pub_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='properties',
            name='pub_date',
            field=models.DateField(default=datetime.datetime(2024, 2, 29, 6, 9, 39, 907326)),
        ),
    ]
