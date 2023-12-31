# Generated by Django 4.2.6 on 2023-10-22 21:30

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_product_product_categories'),
    ]

    operations = [
        migrations.CreateModel(
            name='Watchlists',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_watchlist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auctions.product')),
                ('user_watchlist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=300)),
                ('comment_date_inserted', models.DateField(default=datetime.date.today)),
                ('user_comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Auctions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Amount_bid', models.DecimalField(decimal_places=2, max_digits=12)),
                ('product_sold', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auctions.product')),
                ('user_bid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
