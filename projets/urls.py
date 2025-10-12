from django.urls import path
from . import views

urlpatterns = [
    path('', views.projet_list, name='projet-list'),
    path('<str:pk>/', views.projet_detail, name='projet-detail'),
]
