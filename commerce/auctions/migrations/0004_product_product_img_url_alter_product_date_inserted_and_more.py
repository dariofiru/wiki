# Generated by Django 4.2.6 on 2023-10-22 20:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_product_product_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_img_url',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='date_inserted',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='product',
            name='date_sold',
            field=models.DateField(),
        ),
    ]
