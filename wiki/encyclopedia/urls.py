from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("test/", views.test, name="test"),
    path("wiki/add", views.add, name="add"),
    path("wiki/random", views.random, name="random"),
    path("wiki/modify/<str:id>", views.modify, name="modify"),
    path("wiki/<str:page>", views.page, name="page")


]
