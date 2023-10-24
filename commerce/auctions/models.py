from django.contrib.auth.models import AbstractUser
from multiselectfield import MultiSelectField
from django.db import models
from .models import * 
import datetime
 
class User(AbstractUser):
    pass



class Product(models.Model):
    STATUS_CHOICES = (
    ('active','ACTIVE'),
    ('inactive', 'INACTIVE'),
    ('sold','SOLD')
    )
    CAT_CHOICES = (('Pottery', 'Pottery'),
              ('Sport', 'Sport'),
              ('Forniture', 'Forniture'),
              ('Collectables', 'Collectables'),
              ('Memorabilia', 'Memorabilia'))
    
    product_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=70)
    product_description = models.CharField(max_length=300)
    product_img_url = models.CharField(max_length=500, blank=True, null=True)
    product_categories = MultiSelectField(choices=CAT_CHOICES,
                                 max_choices=3,
                                 max_length=38)


    product_starting_bid = models.DecimalField(decimal_places=2, max_digits=12)
    product_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    date_inserted = models.DateField(default=datetime.date.today)
    date_sold = models.DateField(blank=True, null=True)
    product_price = models.DecimalField(decimal_places=2, max_digits=12, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.product_status != "Sold" and self.product_price != None:
            return  # Yoko shall never have her own blog!
        else:
            super().save(*args, **kwargs)  # Call the "real" save() metho

    def __str__(self) -> str:
        return f"product: {self.product_name}"
    
class Auction(models.Model):
    product_sold = models.ForeignKey(Product, on_delete=models.CASCADE)
    user_bid = models.ForeignKey(User, on_delete=models.CASCADE)
    amount_bid = models.DecimalField(decimal_places=2, max_digits=12)
    winning_bid = models.BooleanField(default=True)
    def __str__(self) -> str:
        return f"Auction: {self.product_sold}"      

class Watchlist(models.Model):
    user_watchlist = models.ForeignKey(User, on_delete=models.CASCADE)
    product_watchlist = models.ForeignKey(Product, on_delete=models.CASCADE)
    def __str__(self) -> str:
        return f"Watchlist: {self.user_watchlist}"    

class Comment(models.Model):
    user_comment = models.ForeignKey(User, on_delete=models.CASCADE)
    product_comment = models.ForeignKey(Product, on_delete=models.CASCADE)
    comment = models.CharField(max_length=300)
    comment_date_inserted = models.DateField(default=datetime.date.today)
    def __str__(self) -> str:
        return f"Comment: {self.user_comment} on {self.product_comment}"    