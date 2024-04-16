# newsaggregator/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('news_list', views.news_list, name='news_list'),
    path('health_list', views.health_list, name='health_list'),
    path('sports_list', views.sports_list, name='sports_list'),
    path('sentiment_list', views.sentiments_list, name='sentiment_list'),
    path('article/<int:article_id>/', views.article_detail, name='article_detail'),
    path('cnn_articles/', views.cnn_articles, name='cnn_articles'),
    path('citizen_digital_articles/', views.citizen_digital_articles,
         name='citizen_digital_articles'),
]
