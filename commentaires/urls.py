from django.urls import path
from . import views

urlpatterns = [
    path('', views.commentaire_list, name='commentaire-list'),
    path('<str:pk>/', views.commentaire_detail, name='commentaire-detail'),
]
