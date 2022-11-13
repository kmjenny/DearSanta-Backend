from django.urls import path, include
from . import views

urlpatterns = [
    path('signup', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('info', views.user_info),
]