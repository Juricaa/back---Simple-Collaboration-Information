from django.urls import path
from . import views

urlpatterns = [
    path('', views.notification_list, name='notification-list'),
    path('<str:pk>/', views.notification_detail, name='notification-detail'),
    path('<str:pk>/marquer-lu/', views.marquer_comme_lu, name='notification-marquer-lu'),
    path('utilisateur/<int:id_utilisateur>/', views.notifications_utilisateur, name='notifications-utilisateur'),
]