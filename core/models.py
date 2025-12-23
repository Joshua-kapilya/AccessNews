from django.db import models

class Article(models.Model):
    title_original = models.TextField()
    title_rewritten = models.TextField()

    description_original = models.TextField(null=True, blank=True)
    description_rewritten = models.TextField(null=True, blank=True)

    content_rewritten = models.TextField(null=True, blank=True)

    image_url = models.URLField(null=True, blank=True)
    source = models.CharField(max_length=100)
    source_url = models.URLField(unique=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title_rewritten
