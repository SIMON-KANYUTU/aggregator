from django.db import models

# Create your models here.


class SentimentAnalysisResult(models.Model):
    article = models.ForeignKey(
        'newsaggregator.Article', on_delete=models.CASCADE)
    sentiment = models.CharField(max_length=10)  # Positive, Negative, Neutral


class HealthSentimentAnalysisResult(models.Model):
    health_article = models.ForeignKey(
        'newsaggregator.Article', on_delete=models.CASCADE)
    sentiment = models.CharField(max_length=10)  # Positive, Negative, Neutral


class SportsSentimentAnalysisResult(models.Model):
    sports_article = models.ForeignKey(
        'newsaggregator.Article', on_delete=models.CASCADE)
    sentiment = models.CharField(max_length=10)  # Positive, Negative, Neutral
