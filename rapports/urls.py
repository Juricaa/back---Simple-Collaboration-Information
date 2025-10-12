from django.urls import path
from . import views

urlpatterns = [
    path('', views.rapport_list, name='rapport-list'),
    path('<str:pk>/', views.rapport_detail, name='rapport-detail'),
]
