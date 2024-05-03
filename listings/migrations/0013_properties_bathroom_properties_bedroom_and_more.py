# Generated by Django 4.0.3 on 2024-03-15 16:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0012_remove_properties_expire_days_properties_expire_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='properties',
            name='bathroom',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='properties',
            name='bedroom',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='properties',
            name='pub_date',
            field=models.DateField(default=datetime.datetime(2024, 3, 15, 16, 30, 33, 918831)),
        ),
    ]
