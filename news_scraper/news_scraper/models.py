from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=255)
    byline = models.TextField()
    time = models.DateTimeField()
    content = models.TextField()

    def __str__(self):
        return self.title
