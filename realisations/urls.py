from django.urls import path
from . import views

urlpatterns = [
    path('', views.realisation_list, name='realisation-list'),
    path('<str:pk>/', views.realisation_detail, name='realisation-detail'),
]
