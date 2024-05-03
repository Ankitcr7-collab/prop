# Generated by Django 4.1 on 2024-02-17 12:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0006_alter_properties_pub_date_savedsearch'),
    ]

    operations = [
        migrations.AlterField(
            model_name='properties',
            name='main_image',
            field=models.FileField(blank=True, null=True, upload_to='properties'),
        ),
        migrations.AlterField(
            model_name='properties',
            name='pub_date',
            field=models.DateField(default=datetime.datetime(2024, 2, 17, 12, 36, 42, 352867)),
        ),
        migrations.AlterField(
            model_name='propertyimage',
            name='images',
            field=models.FileField(blank=True, null=True, upload_to='properties'),
        ),
    ]
