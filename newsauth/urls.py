from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.signup_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('forgot_password/', views.forgot_password_view, name='forgot_password'),
    path('profile_update/', views.profile_update, name='profile_update'),
    path('saved_articles/', views.saved_articles, name='saved_articles'),
    path('save_article/<int:article_id>/',
         views.save_article, name='save_article'),
]
