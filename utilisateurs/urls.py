from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    # 🔹 Authentification
    path('register/', views.RegisterUtilisateurView.as_view(), name='register-utilisateur'),
    path('login/', views.LoginView.as_view(), name='login-utilisateur'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # 🔹 Gestion des utilisateurs
    path('', views.UtilisateurListView.as_view(), name='utilisateur-list'),
    path('<str:pk>/<str:action>/', views.modifier_statut_utilisateur, name='activer-utilisateur'),
    path('<str:pk>/', views.UtilisateurDetailView.as_view(), name='utilisateur-detail'),

    # 🔹 Mot de passe oublié / réinitialisation
    path('password-reset/request/', views.PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('password-reset/confirm/', views.PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
]
