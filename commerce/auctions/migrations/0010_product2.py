# Generated by Django 4.2.6 on 2023-10-24 14:31

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_rename_amount_bid_auction_amount_bid_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product2',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=70)),
                ('product_description', models.CharField(max_length=300)),
                ('product_img_url', models.CharField(blank=True, max_length=500, null=True)),
                ('product_categories', multiselectfield.db.fields.MultiSelectField(choices=[('Pottery', 'Pottery'), ('Sport', 'Sport'), ('Forniture', 'Forniture'), ('Collectables', 'Collectables'), ('Memorabilia', 'Memorabilia')], max_length=38)),
                ('product_starting_bid', models.DecimalField(decimal_places=2, max_digits=12)),
                ('product_status', models.CharField(choices=[('active', 'ACTIVE'), ('inactive', 'INACTIVE'), ('sold', 'SOLD')], default='active', max_length=20)),
                ('date_inserted', models.DateField(default=datetime.date.today)),
                ('date_sold', models.DateField(blank=True, null=True)),
                ('product_price', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('product_bids', models.ManyToManyField(blank=True, related_name='bids', to='auctions.auction')),
                ('product_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
