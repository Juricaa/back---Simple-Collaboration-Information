from django.urls import path
from . import views

urlpatterns = [
    path('', views.region_list, name='region-list'),
    path('<str:pk>/', views.region_detail, name='region-detail'),
]
