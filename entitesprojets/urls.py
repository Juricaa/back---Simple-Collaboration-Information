from django.urls import path
from . import views

urlpatterns = [
    path('', views.entite_projet_list, name='entite-projet-list'),
    path('<int:pk>/', views.entite_projet_detail, name='entite-projet-detail'),
]
