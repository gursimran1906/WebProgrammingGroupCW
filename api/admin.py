from django.contrib import admin
from .models import Category, NewsArticle, UserPreferences, Comment, CustomUser

admin.register(CustomUser)

admin.register(Category)


admin.register(NewsArticle)

admin.register(UserPreferences)
admin.register(Comment)