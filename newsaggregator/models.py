from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=255)
    byline = models.TextField(max_length=255, default="")
    time = models.DateTimeField()
    content = models.TextField()
    sentiment = models.CharField(max_length=20, blank=True, null=True)
    source = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Health(models.Model):
    h_title = models.CharField(max_length=255)
    h_byline = models.TextField(max_length=255, default="")
    h_time = models.DateTimeField()
    h_content = models.TextField()
    h_sentiment = models.CharField(max_length=20, blank=True, null=True)
    h_source = models.CharField(max_length=255)

    def __str__(self):
        return self.h_title


class Sports(models.Model):
    s_title = models.CharField(max_length=255)
    s_byline = models.TextField(max_length=255, default="")
    s_time = models.DateTimeField()
    s_content = models.TextField()
    s_sentiment = models.CharField(max_length=20, blank=True, null=True)
    s_source = models.CharField(max_length=255)

    def __str__(self):
        return self.s_title
