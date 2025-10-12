from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings
import uuid

from .models import Utilisateur
from .serializers import (
    UtilisateurSerializer,
    UtilisateurUpdateSerializer,
    RegisterUtilisateurSerializer,
    LoginSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
)

# ---------------------------------------------------------
# ✅ Enregistrement d'un nouvel utilisateur
# ---------------------------------------------------------
class RegisterUtilisateurView(APIView):
    @swagger_auto_schema(request_body=RegisterUtilisateurSerializer)
    def post(self, request):
        serializer = RegisterUtilisateurSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Compte créé avec succès."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ---------------------------------------------------------
# ✅ Connexion avec JWT
# ---------------------------------------------------------
class LoginView(APIView):
    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(email=email, password=password)

        if user is None:
            try:
                user = Utilisateur.objects.get(email=email)
                if not user.actif:
                    return Response({"error": "Votre compte est désactivé."}, status=status.HTTP_403_FORBIDDEN)
                return Response({"error": "Mot de passe incorrect."}, status=status.HTTP_401_UNAUTHORIZED)
            except Utilisateur.DoesNotExist:
                return Response({"error": "Identifiants invalides."}, status=status.HTTP_401_UNAUTHORIZED)

        # Mise à jour de la dernière connexion
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])

        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "email": user.email,
                "nom": user.nom,
                "role": user.role,
                "id_utilisateur": user.id_utilisateur,
                "id_region": user.id_region.id_region if user.id_region else None,
            }
        })


# ---------------------------------------------------------
# ✅ Liste de tous les utilisateurs
# ---------------------------------------------------------
class UtilisateurListView(APIView):
    permission_classes = []  # Pas de restriction

    def get(self, request):
        utilisateurs = Utilisateur.objects.all()
        serializer = UtilisateurSerializer(utilisateurs, many=True)
        return JsonResponse({
            'success': True,
            'data': serializer.data
        }, status=status.HTTP_200_OK)


# ---------------------------------------------------------
# ✅ Détails, modification et suppression
# ---------------------------------------------------------
class UtilisateurDetailView(APIView):
    permission_classes = []  # Pas de restriction

    def get(self, request, pk):
        try:
            user = Utilisateur.objects.get(pk=pk)
            serializer = UtilisateurSerializer(user)
            return Response(serializer.data)
        except Utilisateur.DoesNotExist:
            return Response({"error": "Utilisateur non trouvé"}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(request_body=UtilisateurUpdateSerializer)
    def put(self, request, pk):
        try:
            user = Utilisateur.objects.get(pk=pk)
            serializer = UtilisateurUpdateSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Utilisateur.DoesNotExist:
            return Response({"error": "Utilisateur non trouvé"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            user = Utilisateur.objects.get(pk=pk)
            user.delete()
            return Response({"message": "Utilisateur supprimé avec succès"}, status=status.HTTP_204_NO_CONTENT)
        except Utilisateur.DoesNotExist:
            return Response({"error": "Utilisateur non trouvé"}, status=status.HTTP_404_NOT_FOUND)


# ---------------------------------------------------------
# ✅ Vérification (activation) d’un utilisateur
# ---------------------------------------------------------
@api_view(['PATCH', 'POST'])
# views.py
def modifier_statut_utilisateur(request, pk, action):
    try:
        user = Utilisateur.objects.get(pk=pk)
        
        if action == 'activer':
            user.actif = True
            message = "Utilisateur activé avec succès"
        elif action == 'desactiver':
            user.actif = False
            message = "Utilisateur désactivé avec succès"
        else:
            return Response({"error": "Action non valide"}, status=status.HTTP_400_BAD_REQUEST)
        
        user.save()
        return Response({"message": message}, status=status.HTTP_200_OK)
        
    except Utilisateur.DoesNotExist:
        return Response({"error": "Utilisateur non trouvé"}, status=status.HTTP_404_NOT_FOUND)


# ---------------------------------------------------------
# ✅ Réinitialisation du mot de passe
# ---------------------------------------------------------
class PasswordResetRequestView(APIView):
    @swagger_auto_schema(request_body=PasswordResetRequestSerializer)
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']

            try:
                user = Utilisateur.objects.get(email=email)
            except Utilisateur.DoesNotExist:
                return Response({"message": "Si cet email existe, un lien a été envoyé."}, status=status.HTTP_200_OK)

            token = uuid.uuid4().hex
            user.reset_password_token = token
            user.reset_password_token_expires = timezone.now() + timedelta(minutes=15)
            user.save()

            reset_url = f"{settings.FRONTEND_URL}/reset-password/{token}"
            send_mail(
                "Réinitialisation de mot de passe",
                f"Cliquez ici pour réinitialiser : {reset_url}",
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )

            return Response({"message": "Si cet email existe, un lien a été envoyé."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmView(APIView):
    @swagger_auto_schema(request_body=PasswordResetConfirmSerializer)
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data['token']
            new_password = serializer.validated_data['new_password']

            try:
                user = Utilisateur.objects.get(reset_password_token=token)
            except Utilisateur.DoesNotExist:
                return Response({"error": "Token invalide ou expiré"}, status=status.HTTP_400_BAD_REQUEST)

            if user.reset_password_token_expires < timezone.now():
                return Response({"error": "Token expiré"}, status=status.HTTP_400_BAD_REQUEST)

            user.mot_de_passe = make_password(new_password)
            user.reset_password_token = None
            user.reset_password_token_expires = None
            user.save()

            return Response({"message": "Mot de passe réinitialisé avec succès"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
