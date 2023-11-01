from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add", views.add, name="add"),
    path("categories", views.categories, name="categories"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories/<str:id>", views.category_chosen, name="category_chosen") ,
    #path("auctions/bid/accept_bid/<str:id>", views.accept_bid, name="accept_bid") ,
    path("auctions/watchlist/add/<str:id>", views.add_watchlist, name="add_watchlist"),
    path("auctions/watchlist/remove/<str:id>", views.remove_watchlist, name="remove_watchlist"),
    path("auctions/open_listing/<str:id>", views.open_listing, name="open_listing"),
    path("auctions/open_listing/accept_bid/<str:id>", views.accept_bid, name="accept_bid")
    #path("auctions/bid/<str:id>", views.bid, name="bid")
    
    
]
