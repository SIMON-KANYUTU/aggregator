from django.urls import path
from newsmain import views


urlpatterns = [
    path('', views.index, name="index"),
]
