from django.urls import path
from . import views

urlpatterns = [
    path('', views.axe_list, name='axe-list'),
    path('<str:pk>/', views.axe_detail, name='axe-detail'),
]
