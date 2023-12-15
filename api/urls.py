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
from django.conf.urls.static import static
from django.http import HttpResponse

from django.urls import path
from .views import signup_view, delete_comment, edit_comment, parent_comment_list, child_comments_list, login_view, user_logout, update_profile, news_list, article_detail, add_comment_to_article, add_reply_to_comment, add_article, main_spa, get_user_details, all_categories, user_preferences, save_user_preferences

urlpatterns = [
   
    path('', main_spa),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path("signout/",user_logout,name="signout"),
    
    path('api/user_details/', get_user_details, name='user details'),
    path('api/update_profile/', update_profile, name='profile_update'),
    path('api/news/', news_list, name='news_list'),
    path('api/all_categories/', all_categories, name='all_categories'),
    path('api/user_preferences/', user_preferences, name='user_preferences'),
    path('api/save_user_preferences/', save_user_preferences, name='save_user_preferences'),


    path('api/get_comments/<int:article_id>/',parent_comment_list , name='comments_article'),
    path('api/get_child_comments/<int:article_id>/',child_comments_list, name='child_comments_article'),   
    path('api/article/<int:article_id>/', article_detail, name='article_detail'),
    path('api/article/<int:article_id>/add_comment/', add_comment_to_article, name='add_comment_to_article'),
    path('api/comment/<int:parent_comment_id>/add_reply/', add_reply_to_comment, name='add_reply_to_comment'),
    path('api/add_article/', add_article, name='add_article'),
    path('api/comment/<int:comment_id>/edit_comment/', edit_comment, name='edit_comment'),
    path('api/comment/<int:comment_id>/delete/', delete_comment, name='delete_comment'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

