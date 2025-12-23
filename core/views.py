from django.shortcuts import render
from .models import Article

def home(request):
    # Latest 20 articles
    articles = Article.objects.order_by('-created_at')[:20]
    return render(request, "core/home.html", {"articles": articles})

def article_detail(request, id):
    from django.shortcuts import get_object_or_404
    from .models import Article
    article = get_object_or_404(Article, id=id)
    return render(request, "core/article_detail.html", {"article": article})
