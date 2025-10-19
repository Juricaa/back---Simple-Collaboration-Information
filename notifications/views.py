from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema

from .models import Notification
from .serializers import NotificationSerializer


# ---------------------------------------------------------
# ✅ Liste des notifications + création
# ---------------------------------------------------------
@swagger_auto_schema(method='post', request_body=NotificationSerializer, responses={201: NotificationSerializer})
@api_view(['GET', 'POST'])
def notification_list(request):
    if request.method == 'GET':
        notifications = Notification.objects.all()

        # 🔍 Filtrage optionnel par utilisateur
        id_utilisateur = request.GET.get('id_utilisateur', None)
        if id_utilisateur is not None:
            notifications = notifications.filter(id_utilisateur=id_utilisateur)

        # 🔍 Filtrage optionnel par type
        type_notification = request.GET.get('type', None)
        if type_notification is not None:
            notifications = notifications.filter(type=type_notification)

        # 🔍 Filtrage optionnel par statut de lecture
        est_lu = request.GET.get('est_lu', None)
        if est_lu is not None:
            est_lu_bool = est_lu.lower() in ['true', '1', 'yes']
            notifications = notifications.filter(est_lu=est_lu_bool)

        # 🔍 Filtrage optionnel par titre
        titre = request.GET.get('titre', None)
        if titre is not None:
            notifications = notifications.filter(titre__icontains=titre)

        serializer = NotificationSerializer(notifications, many=True)
        return JsonResponse(
            {
                'success': True,
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = NotificationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(
                {
                    'success': True,
                    'message': 'Notification créée avec succès',
                    'data': serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ---------------------------------------------------------
# ✅ Détails / Modification / Suppression d'une notification
# ---------------------------------------------------------
@swagger_auto_schema(method='put', request_body=NotificationSerializer, operation_description="Met à jour une notification")
@swagger_auto_schema(method='delete', operation_description="Supprime une notification par ID")
@api_view(['GET', 'PUT', 'DELETE'])
def notification_detail(request, pk):
    try:
        notification = Notification.objects.get(pk=pk)
    except Notification.DoesNotExist:
        return JsonResponse({'message': 'Notification introuvable'}, status=status.HTTP_404_NOT_FOUND)

    # 🔹 Récupération d'une notification
    if request.method == 'GET':
        serializer = NotificationSerializer(notification)
        return JsonResponse(
            {
                'success': True,
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )

    # 🔹 Mise à jour d'une notification
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = NotificationSerializer(notification, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(
                {
                    'success': True,
                    'message': 'Notification mise à jour avec succès',
                    'data': serializer.data
                },
                status=status.HTTP_200_OK
            )
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 🔹 Suppression d'une notification
    elif request.method == 'DELETE':
        notification.delete()
        return JsonResponse(
            {'message': 'Notification supprimée avec succès'},
            status=status.HTTP_204_NO_CONTENT
        )


# ---------------------------------------------------------
# ✅ Marquer une notification comme lue
# ---------------------------------------------------------
@swagger_auto_schema(method='patch', operation_description="Marque une notification comme lue")
@api_view(['PATCH'])
def marquer_comme_lu(request, pk):
    try:
        notification = Notification.objects.get(pk=pk)
    except Notification.DoesNotExist:
        return JsonResponse({'message': 'Notification introuvable'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PATCH':
        notification.est_lu = True
        notification.save()
        
        serializer = NotificationSerializer(notification)
        return JsonResponse(
            {
                'success': True,
                'message': 'Notification marquée comme lue',
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )


# ---------------------------------------------------------
# ✅ Notifications par utilisateur
# ---------------------------------------------------------
@api_view(['GET'])
def notifications_utilisateur(request, id_utilisateur):
    if request.method == 'GET':
        notifications = Notification.objects.filter(id_utilisateur=id_utilisateur).order_by('-date_creation')
        
        # 🔍 Filtrage optionnel par statut de lecture
        est_lu = request.GET.get('est_lu', None)
        if est_lu is not None:
            est_lu_bool = est_lu.lower() in ['true', '1', 'yes']
            notifications = notifications.filter(est_lu=est_lu_bool)
        
        # 🔍 Filtrage optionnel par type
        type_notification = request.GET.get('type', None)
        if type_notification is not None:
            notifications = notifications.filter(type=type_notification)
        
        serializer = NotificationSerializer(notifications, many=True)
        return JsonResponse(
            {
                'success': True,
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )