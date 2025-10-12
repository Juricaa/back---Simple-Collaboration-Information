from rest_framework import serializers
from .models import Utilisateur

class UtilisateurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateur
        fields = '__all__'

class UtilisateurUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateur
        fields = ['nom', 'email', 'role', 'actif', 'id_region']

class RegisterUtilisateurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateur
        fields = ['nom', 'email', 'mot_de_passe', 'id_region', 'role']

    def create(self, validated_data):
        user = Utilisateur(
            email=validated_data['email'],
            nom=validated_data.get('nom'),
            id_region=validated_data.get('id_region'),
            role=validated_data.get('role'),
        )
        user.set_password(validated_data['mot_de_passe'])
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.CharField()
    new_password = serializers.CharField()
