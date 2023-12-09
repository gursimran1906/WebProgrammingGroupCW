"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.http import HttpResponse

from django.urls import path
from .views import profile, news_list, article_detail, add_comment_to_article, add_reply_to_comment, add_article

urlpatterns = [
    path('profile/', profile, name='profile'),
    path('news/', news_list, name='news_list'),
    path('article/<int:article_id>/', article_detail, name='article_detail'),
    path('article/<int:article_id>/add_comment/', add_comment_to_article, name='add_comment_to_article'),
    path('article/<int:article_id>/comment/<int:parent_comment_id>/add_reply/', add_reply_to_comment, name='add_reply_to_comment'),
    path('add_article/', add_article, name='add_article'),
   
]

