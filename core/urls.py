# news/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("article/<int:id>/", views.article_detail, name="article_detail"),
]
