# Generated by Django 4.0.3 on 2024-02-29 05:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0008_alter_properties_pub_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='properties',
            name='pub_date',
            field=models.DateField(default=datetime.datetime(2024, 2, 29, 5, 40, 40, 535784)),
        ),
    ]
