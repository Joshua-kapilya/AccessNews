from django.db import models
from django.contrib.auth.models import User


class Article(models.Model):
    CATEGORY_CHOICES = [
        ("Politics", "Politics"),
        ("Business", "Business"),
        ("Sports", "Sports"),
        ("Technology", "Technology"),
        ("Entertainment", "Entertainment"),
        ("Health", "Health"),
        ("Other", "Other"),
    ]

    title_original = models.TextField()
    title_rewritten = models.TextField()

    description_original = models.TextField(null=True, blank=True)
    description_rewritten = models.TextField(null=True, blank=True)

    content_rewritten = models.TextField(null=True, blank=True)

    image_url = models.URLField(null=True, blank=True)
    source = models.CharField(max_length=100)
    source_url = models.URLField(unique=True)

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default="Other"
    )

    # ✅ NEW
    views = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title_rewritten


# ==============================
# 💬 COMMENTS + REPLIES
# ==============================

class Comment(models.Model):
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        related_name="replies",
        on_delete=models.CASCADE
    )

    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user} on {self.article}"


# ==============================
# 👍 👎 LIKES / DISLIKES
# ==============================

class Reaction(models.Model):
    REACTION_CHOICES = [
        ("like", "Like"),
        ("dislike", "Dislike"),
    ]

    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name="reactions"
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    reaction = models.CharField(max_length=10, choices=REACTION_CHOICES)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("article", "user")

    def __str__(self):
        return f"{self.user} {self.reaction} {self.article}"
