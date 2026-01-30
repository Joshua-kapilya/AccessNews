# news/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("article/<int:id>/", views.article_detail, name="article_detail"),path("privacy-policy/", views.privacy_policy, name="privacy_policy"),
    path("about-us/", views.about_us, name="about_us"),
    path("privacy-policy/", views.privacy_policy, name="privacy_policy"),
    path("about-us/", views.about_us, name="about_us"),
]
