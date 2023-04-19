
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:user>", views.profile, name="profile"),
    path("following_posts/<str:user>", views.following_posts, name="following_posts"),

    # API Routes
    path("like/<int:id>", views.like, name="like"),
    path("post/<int:id>", views.edit_post, name="edit_post"),
    path("save_edit/<int:id>", views.save_edit, name="save_edit")
]
