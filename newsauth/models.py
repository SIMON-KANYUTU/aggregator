from django.db import models
from django.contrib.auth.models import User
from newsaggregator.models import Article
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add fields for additional user details like name, bio, etc.
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username


class SavedArticle(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s saved article: {self.article.title}"
