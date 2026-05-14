from django.urls import path
from . import views

urlpatterns = [
    path('newsfeed/', views.get_articles),
    path('newsfeed/search', views.search_articles),
    path('bookmarks/', views.get_bookmarks),
    path('bookmarks/search', views.search_bookmarks),
    path('bookmarks/+/', views.bookmark_article),
    path('bookmarks/<int:id>/', views.remove_bookmark),
    path('tags/', views.get_tags),
    path('followedtags/', views.get_user_tags),
    path('ignoredtags/', views.get_ignored_user_tags),
    path('followedtags/+/', views.set_user_tag),
    path('ignoredtags/+/', views.set_ignored_user_tag),
    path('followedtags/<int:id>/', views.remove_user_tag),
    path('ignoredtags/<int:id>/', views.remove_ignored_user_tag),
    path('publications/',  views.get_publications),
    path('followedpublications/', views.get_user_publications),
    path('followedpublications/+/', views.set_user_publication),
    path('followedpublications/<int:id>/', views.remove_user_publication),
    
]