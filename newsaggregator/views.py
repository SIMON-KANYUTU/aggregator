from django.shortcuts import render, get_object_or_404
from .models import Article, Health, Sports
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from news_sentiments.utils import predict_sentiment
from news_sentiments.models import SentimentAnalysisResult


def news_list(request):
    articles = Article.objects.all()

    # Randomly order the articles
    articles = articles.order_by('?')

    # Truncate the content of each article to 250 characters
    for article in articles:
        article.content = article.content[:250] + \
            '...' if len(article.content) > 250 else article.content

    # paginator
    paginator = Paginator(articles, 4)  # Limit 4 articles per page
    page_number = request.GET.get('page')
    try:
        articles = paginator.page(page_number)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    context = {
        'articles': articles

    }
    return render(request, 'newsaggregator/news_list.html', context)


def article_detail(request, article_id):
    # Retrieve the article object using its ID
    article = get_object_or_404(Article, pk=article_id)
    return render(request, 'newsaggregator/article_detail.html', {'article': article})


def health_list(request):
    healtharticles = Health.objects.all()

    # Randomly order the articles
    healtharticles = healtharticles.order_by('?')

    paginator = Paginator(healtharticles, 2)  # Limit 2 articles per page

    page_number = request.GET.get('page')
    try:
        healtharticles = paginator.page(page_number)
    except PageNotAnInteger:
        healtharticles = paginator.page(1)
    except EmptyPage:
        healtharticles = paginator.page(paginator.num_pages)

    context = {
        'healtharticles': healtharticles
    }
    return render(request, 'newsaggregator/health_list.html', context)


def sports_list(request):
    sportsarticles = Sports.objects.all()

    # Randomly order the articles
    sportsarticles = sportsarticles.order_by('?')

    # Paginator
    paginator = Paginator(sportsarticles, 2)  # Limit 2 articles per page

    page_number = request.GET.get('page')
    try:
        sportsarticles = paginator.page(page_number)
    except PageNotAnInteger:
        sportsarticles = paginator.page(1)
    except EmptyPage:
        sportsarticles = paginator.page(paginator.num_pages)

    context = {
        'sportsarticles': sportsarticles
    }
    return render(request, 'newsaggregator/sports_list.html', context)


def sentiments_list(request):
    articles = Article.objects.all()
    # Predict sentiment for each article and save the results
    for article in articles:
        sentiment = predict_sentiment(article.content)
        SentimentAnalysisResult.objects.create(
            article=article, sentiment=sentiment)

    # Retrieve sentiment analysis results
    sentiment_results = {article.id: SentimentAnalysisResult.objects.get(
        article=article).sentiment for article in articles}

    context = {
        # Include sentiment_results in the context dictionary
        'sentiment_results': sentiment_results
    }
    return render(request, 'newsaggregator/sentiment_list.html', context)


# views.py

def cnn_articles(request):
    # Filter articles from the CNN source
    cnn_articles = Article.objects.filter(source='CNN')

    # Randomly order the articles
    cnn_articles = cnn_articles.order_by('?')

    # Truncate the content of each article to 250 characters
    for article in cnn_articles:
        article.content = article.content[:250] + \
            '...' if len(article.content) > 250 else article.content

    # Render the CNN articles in a template
    return render(request, 'newsaggregator/cnn_articles.html', {'cnn_articles': cnn_articles})


def citizen_digital_articles(request):
    citizen_digital_articles = Article.objects.filter(source='Citizen Digital')

    # Randomly order the articles
    citizen_digital_articles = citizen_digital_articles.order_by('?')

    # Truncate the content of each article to 250 characters
    for article in citizen_digital_articles:
        article.content = article.content[:250] + \
            '...' if len(article.content) > 250 else article.content

    # Render the Citizen Digital articles in a template
    return render(request, 'newsaggregator/citizen_digital_articles.html', {'citizen_digital_articles': citizen_digital_articles})
