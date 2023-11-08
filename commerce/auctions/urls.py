from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.createNew, name = "new"),
    path("addToWatchlist/<str:title>", views.addTowatchlist, name = "addTowatchlist"),
    path("like/<int:id>/<str:name>", views.like, name = "like"),
    path("watchlist", views.watchlist, name = "watchlist"),
    path("place_bid/<str:title>", views.place_bid, name= "place_bid"),
    path("close/<str:title>", views.close, name = "close"),
    path("comment/<str:title>", views.comment, name = "comment"),
    path("categories", views.categories, name = "categories"),
    path("<int:id>", views.category_items,name="category_items"),
    path("profiles/<str:username>", views.profile, name = "profile"),
    path("<str:title>", views.listing, name = "title")
]
