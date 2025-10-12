from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser  # type: ignore
from rest_framework import status  # type: ignore
from rest_framework.decorators import api_view  # type: ignore
from drf_yasg.utils import swagger_auto_schema

from .models import Region
from .serializers import RegionSerializer


# ---------------------------------------------------------
# ✅ Liste des régions + création
# ---------------------------------------------------------
@swagger_auto_schema(method='post', request_body=RegionSerializer, responses={201: RegionSerializer})
@api_view(['GET', 'POST'])
def region_list(request):
    if request.method == 'GET':
        regions = Region.objects.all()

        # 🔍 Filtrage optionnel par nom
        nom = request.GET.get('nom', None)
        if nom is not None:
            regions = regions.filter(nom__icontains=nom)

        serializer = RegionSerializer(regions, many=True)
        return JsonResponse(
            {
                'success': True,
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = RegionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(
                {
                    'success': True,
                    'message': 'Région créée avec succès',
                    'data': serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ---------------------------------------------------------
# ✅ Détails / Modification / Suppression d’une région
# ---------------------------------------------------------
@swagger_auto_schema(method='put', request_body=RegionSerializer, operation_description="Met à jour une région")
@swagger_auto_schema(method='delete', operation_description="Supprime une région par ID")
@api_view(['GET', 'PUT', 'DELETE'])
def region_detail(request, pk):
    try:
        region = Region.objects.get(pk=pk)
    except Region.DoesNotExist:
        return JsonResponse({'message': 'Région introuvable'}, status=status.HTTP_404_NOT_FOUND)

    # 🔹 Récupération d’une région
    if request.method == 'GET':
        serializer = RegionSerializer(region)
        return JsonResponse(
            {
                'success': True,
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )

    # 🔹 Mise à jour d’une région
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = RegionSerializer(region, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(
                {
                    'success': True,
                    'message': 'Région mise à jour avec succès',
                    'data': serializer.data
                },
                status=status.HTTP_200_OK
            )
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 🔹 Suppression d’une région
    elif request.method == 'DELETE':
        region.delete()
        return JsonResponse(
            {'message': 'Région supprimée avec succès'},
            status=status.HTTP_204_NO_CONTENT
        )
