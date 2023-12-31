# Generated by Django 4.2.6 on 2023-10-22 20:34

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_alter_product_date_sold_alter_product_product_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_categories',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('Pottery', 'Pottery'), ('Sport', 'Sport'), ('Forniture', 'Forniture'), ('Collectables', 'Collectables'), ('Memorabilia', 'Memorabilia')], default=2, max_length=38),
            preserve_default=False,
        ),
    ]
