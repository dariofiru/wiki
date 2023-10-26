from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add", views.add, name="add"),
    path("auctions/bid/accept_bid/<str:id>", views.accept_bid, name="accept_bid") ,
    path("auctions/bid/<str:id>", views.bid, name="bid")
    
    
]
