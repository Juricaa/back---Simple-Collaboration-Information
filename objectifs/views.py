from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser  # type: ignore
from rest_framework import status  # type: ignore
from rest_framework.decorators import api_view  # type: ignore
from drf_yasg.utils import swagger_auto_schema

from objectifs.models import Objectif
from axes.serializers import ObjectifSerializer


# ✅ Liste et création des objectifs
@swagger_auto_schema(method='post', request_body=ObjectifSerializer, responses={201: ObjectifSerializer})
@api_view(['GET', 'POST'])
def objectif_list(request):
    if request.method == 'GET':
        objectifs = Objectif.objects.all()

        intitule = request.GET.get('intitule', None)
        if intitule is not None:
            objectifs = objectifs.filter(intitule__icontains=intitule)

        serializer = ObjectifSerializer(objectifs, many=True)
        return JsonResponse(
            {
                'success': True,
                'data': serializer.data
            }, status=status.HTTP_200_OK
        )

    elif request.method == 'POST':
        serializer = ObjectifSerializer(data=request.data)
        # data = JSONParser().parse(request)
        # serializer = ObjectifSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(
                {
                    'success': True,
                    'data': serializer.data
                }, status=status.HTTP_201_CREATED
            )
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ✅ Détail, mise à jour et suppression d’un objectif
@swagger_auto_schema(method='put', request_body=ObjectifSerializer, operation_description="Met à jour un objectif")
@swagger_auto_schema(method='delete', operation_description="Supprime un objectif par ID")
@api_view(['GET', 'PUT', 'DELETE'])
def objectif_detail(request, pk):
    try:
        objectif = Objectif.objects.get(pk=pk)
    except Objectif.DoesNotExist:
        return JsonResponse({'message': 'Objectif non trouvé'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ObjectifSerializer(objectif)
        return JsonResponse(
            {
                'success': True,
                'data': serializer.data
            }, status=status.HTTP_200_OK
        )

    elif request.method == 'PUT':
        serializer = ObjectifSerializer(objectif, data=request.data, partial=True)
        # data = JSONParser().parse(request)
        # serializer = ObjectifSerializer(objectif, data=data)
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
        objectif.delete()
        return JsonResponse({'message': 'Objectif supprimé avec succès !'}, status=status.HTTP_204_NO_CONTENT)
