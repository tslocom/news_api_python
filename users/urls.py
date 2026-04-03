from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.create_user),
    path('login/', views.login_user)
]
