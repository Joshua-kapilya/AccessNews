from django.shortcuts import render, get_object_or_404
from .models import Article

CATEGORY_LIST = ["Politics", "Business", "Sports", "Technology", "Entertainment", "Health", "Other"]

def home(request):
    category = request.GET.get("category")

    if category:
        articles = Article.objects.filter(category=category).order_by('-created_at')[:20]
    else:
        articles = Article.objects.order_by('-created_at')[:20]

    context = {
        "articles": articles,
        "selected_category": category,
        "categories": CATEGORY_LIST  # <-- pass categories to template
    }

    return render(request, "core/home.html", context)


def article_detail(request, id):
    article = get_object_or_404(Article, id=id)
    return render(request, "core/article_detail.html", {"article": article})



def privacy_policy(request):
    return render(request, "core/privacy_policy.html")

def about_us(request):
    return render(request, "core/about_us.html")


