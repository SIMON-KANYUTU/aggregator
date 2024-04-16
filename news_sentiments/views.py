from django.shortcuts import render, redirect
from .models import SentimentAnalysisResult, HealthSentimentAnalysisResult, SportsSentimentAnalysisResult
from newsaggregator.models import Article, Health, Sports
from .utils import predict_sentiment
from django.urls import reverse


def analyze_sentiment(article_id):
    article = Article.objects.get(pk=article_id)
    sentiment = predict_sentiment(article.content)

    # Check if a sentiment analysis result already exists for this article
    existing_results = SentimentAnalysisResult.objects.filter(article=article)

    if existing_results.exists():
        # Update the existing result if it exists
        existing_result = existing_results.first()
        existing_result.sentiment = sentiment
        existing_result.save()
    else:
        # Create a new sentiment analysis result if none exists
        SentimentAnalysisResult.objects.create(
            article=article, sentiment=sentiment)


def analyze_health_sentiment(health_id):
    health_article = Health.objects.get(pk=health_id)
    sentiment = predict_sentiment(health_article.h_content)

    # Check if a sentiment analysis result already exists for this health article
    existing_results = HealthSentimentAnalysisResult.objects.filter(
        article=health_article)

    if existing_results.exists():
        # Update the existing result if it exists
        existing_result = existing_results.first()
        existing_result.sentiment = sentiment
        existing_result.save()
    else:
        # Create a new sentiment analysis result if none exists
        HealthSentimentAnalysisResult.objects.create(
            article=health_article, sentiment=sentiment)


def analyze_sports_sentiment(sports_id):
    sports_article = Sports.objects.get(pk=sports_id)
    sentiment = predict_sentiment(sports_article.s_content)

    # Check if a sentiment analysis result already exists for this sports article
    existing_results = SportsSentimentAnalysisResult.objects.filter(
        article=sports_article)

    if existing_results.exists():
        # Update the existing result if it exists
        existing_result = existing_results.first()
        existing_result.sentiment = sentiment
        existing_result.save()
    else:
        # Create a new sentiment analysis result if none exists
        SportsSentimentAnalysisResult.objects.create(
            article=sports_article, sentiment=sentiment)
