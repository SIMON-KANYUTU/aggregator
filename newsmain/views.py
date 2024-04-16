from django.shortcuts import render, get_object_or_404
from datetime import datetime
from django.http import HttpResponse
from newsaggregator.models import Article, Health, Sports

# Create your views here.


def index(request):
    current_datetime = datetime.now()
    articles = Article.objects.all()
    total_articles = Article.objects.count()
    healtharticles = Health.objects.all()
    health_total_articles = Health.objects.count()
    sportsarticles = Sports.objects.all()
    sports_total_articles = Sports.objects.count()

    # Randomly order the articles
    articles = articles.order_by('?')

    context = {
        'articles': articles,
        'current_datetime': current_datetime,
        'total_articles': total_articles,
        'healtharticles': healtharticles,
        'health_total_articles': health_total_articles,
        'sportsarticles': sportsarticles,
        'sports_total_articles': sports_total_articles,
    }
    return render(request, "index.html", context)


def article_detail(request, article_id):
    # Retrieve the article object using its ID
    article = get_object_or_404(Article, pk=article_id)
    return render(request, 'newsaggregator/article_detail.html', {'article': article})
