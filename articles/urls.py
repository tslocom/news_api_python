from django.urls import path
from . import views

urlpatterns = [
    path('newsfeed/', views.get_articles),
]