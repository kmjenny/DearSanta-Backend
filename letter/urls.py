from django.urls import path, include
from . import views

urlpatterns = [
    path('write', views.write_letter),
    path('answer', views.write_answer),
    path('', views.get_letter),
]