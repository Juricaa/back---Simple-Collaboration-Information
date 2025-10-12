from django.urls import path
from . import views

urlpatterns = [
    path('', views.objectif_list, name='objectif-list'),
    path('<str:pk>/', views.objectif_detail, name='objectif-detail'),
]
