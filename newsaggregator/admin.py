# admin.py
from django.contrib import admin
from .models import Article, Health, Sports

# Register your models here.


admin.site.register(Article)
admin.site.register(Health)
admin.site.register(Sports)
