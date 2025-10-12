from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser  # type: ignore
from rest_framework import status  # type: ignore
from rest_framework.decorators import api_view  # type: ignore
from drf_yasg.utils import swagger_auto_schema

from entites.models import Entite
from .serializers import EntiteSerializer


# ✅ Liste et création des entités
@swagger_auto_schema(method='post', request_body=EntiteSerializer, responses={201: EntiteSerializer})
@api_view(['GET', 'POST'])
def entite_list(request):
    if request.method == 'GET':
        entites = Entite.objects.all()

        nom = request.GET.get('nom', None)
        if nom is not None:
            entites = entites.filter(nom__icontains=nom)

        serializer = EntiteSerializer(entites, many=True)
        return JsonResponse(
            {
                'success': True,
                'data': serializer.data
            }, status=status.HTTP_200_OK
        )

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = EntiteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(
                {
                    'success': True,
                    'data': serializer.data
                }, status=status.HTTP_201_CREATED
            )
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ✅ Détail, mise à jour et suppression d’une entité
@swagger_auto_schema(method='put', request_body=EntiteSerializer, operation_description="Met à jour une entité")
@swagger_auto_schema(method='delete', operation_description="Supprime une entité par ID")
@api_view(['GET', 'PUT', 'DELETE'])
def entite_detail(request, pk):
    try:
        entite = Entite.objects.get(pk=pk)
    except Entite.DoesNotExist:
        return JsonResponse({'message': 'Entité non trouvée'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = EntiteSerializer(entite)
        return JsonResponse(
            {
                'success': True,
                'data': serializer.data
            }, status=status.HTTP_200_OK
        )

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = EntiteSerializer(entite, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(
                {
                    'success': True,
                    'data': serializer.data
                }, status=status.HTTP_200_OK
            )
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        entite.delete()
        return JsonResponse({'message': 'Entité supprimée avec succès !'}, status=status.HTTP_204_NO_CONTENT)
