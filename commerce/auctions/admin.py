from django.contrib import admin
from .models import Auction, Comment, User, Watchlist, Product2
from .models import Product

# Register your models here.
admin.site.register(User)

admin.site.register(Product)
admin.site.register(Comment)
admin.site.register(Watchlist)
admin.site.register(Auction)
admin.site.register(Product2    )
