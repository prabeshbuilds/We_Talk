from django.urls import path
from . import views

urlpatterns = [
    path('', views.api_root),
    path('register/', views.register),
    path('login/', views.login),
    path('discover/', views.discover_users),
    path('connect/<int:user_id>/', views.send_request),
]