from django.urls import path
from . import views

urlpatterns = [
    path('', views.entite_list, name='entite-list'),
    path('<str:pk>/', views.entite_detail, name='entite-detail'),
]
