# news/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("article/<int:id>/", views.article_detail, name="article_detail"),path("privacy-policy/", views.privacy_policy, name="privacy_policy"),
    path("about-us/", views.about_us, name="about_us"),
    path("privacy-policy/", views.privacy_policy, name="privacy_policy"),
    path("about-us/", views.about_us, name="about_us"),
    path("article/<int:id>/comment/", views.add_comment, name="add_comment"),
    path(
        "article/<int:id>/react/<str:reaction_type>/",
        views.react_article,
        name="react_article"
    ),
    path("comment/<int:comment_id>/reply/", views.add_reply, name="add_reply"),
    path("search/", views.search_articles, name="search_articles"),

]
