from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import F
from .models import Article, Comment, Reaction

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
        "categories": CATEGORY_LIST
    }

    return render(request, "core/home.html", context)


def article_detail(request, id):
    article = get_object_or_404(Article, id=id)

    # ✅ Increment views safely
    Article.objects.filter(id=id).update(views=F("views") + 1)
    article.refresh_from_db()

    # ✅ Load top-level comments
    comments = article.comments.filter(parent__isnull=True).order_by('-created_at')

    # ✅ Count likes and dislikes
    likes = article.reactions.filter(reaction="like").count()
    dislikes = article.reactions.filter(reaction="dislike").count()

    context = {
        "article": article,
        "comments": comments,
        "likes": likes,
        "dislikes": dislikes,
    }

    return render(request, "core/article_detail.html", context)


def privacy_policy(request):
    return render(request, "core/privacy_policy.html")


def about_us(request):
    return render(request, "core/about_us.html")




from django.contrib.auth.models import User
from django.utils.crypto import get_random_string


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from .models import Article, Comment


def add_comment(request, id):
    article = get_object_or_404(Article, id=id)

    if request.method == "POST":
        content = request.POST.get("content")
        parent_id = request.POST.get("parent_id")

        parent = None
        if parent_id:
            parent = Comment.objects.filter(id=parent_id).first()

        # ✅ if logged in → use them
        if request.user.is_authenticated:
            user = request.user
        else:
            # ✅ fallback guest account
            username = f"guest_{get_random_string(8)}"

            # Create guest user with unusable password
            user, _ = User.objects.get_or_create(
                username=username
            )
            user.set_unusable_password()
            user.save()

        if content:
            Comment.objects.create(
                article=article,
                user=user,
                content=content,
                parent=parent
            )

    return redirect("article_detail", id=id)


def react_article(request, id, reaction_type):
    article = get_object_or_404(Article, id=id)

    reaction, created = Reaction.objects.get_or_create(
        article=article,
        user=request.user,
        defaults={"reaction": reaction_type}
    )

    if not created:
        if reaction.reaction == reaction_type:
            reaction.delete()
        else:
            reaction.reaction = reaction_type
            reaction.save()

    return redirect("article_detail", id=id)


from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from .models import Comment, Article

def add_reply(request, comment_id):
    parent_comment = get_object_or_404(Comment, id=comment_id)
    article = parent_comment.article

    if request.method == "POST":
        content = request.POST.get("content")

        # ✅ Determine user (authenticated or guest)
        if request.user.is_authenticated:
            user = request.user
        else:
            username = f"guest_{get_random_string(8)}"
            user, _ = User.objects.get_or_create(username=username)
            user.set_unusable_password()
            user.save()

        if content:
            Comment.objects.create(
                article=article,
                user=user,
                content=content,
                parent=parent_comment
            )

    return redirect("article_detail", id=article.id)


from django.db.models import Q

def search_articles(request):
    query = request.GET.get("q", "")  # Get search term from input
    articles = []

    if query:
        # Search in title_rewritten and content_rewritten
        articles = Article.objects.filter(
            Q(title_rewritten__icontains=query) |
            Q(content_rewritten__icontains=query)
        ).order_by('-created_at')

    context = {
        "articles": articles,
        "query": query,
        "categories": CATEGORY_LIST,
    }

    return render(request, "core/search_results.html", context)
