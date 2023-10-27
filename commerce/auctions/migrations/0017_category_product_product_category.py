# Generated by Django 4.2.6 on 2023-10-27 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0016_auction_date_bid_alter_comment_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=40)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='product_category',
            field=models.ManyToManyField(to='auctions.category'),
        ),
    ]