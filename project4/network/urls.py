
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("post", views.post, name = "post"),
    path("following", views.following, name = "following"),
    path("<str:name>", views.profile, name = "profile"),
    path("post/edit/<int:id>", views.edit, name = "edit"),
     path('like_post/<int:post_id>/', views.like_post, name='like_post'),
    
]
