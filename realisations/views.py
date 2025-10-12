from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser  # type: ignore
from rest_framework import status  # type: ignore
from rest_framework.decorators import api_view  # type: ignore
from drf_yasg.utils import swagger_auto_schema

from realisations.models import Realisation
from .serializers import RealisationSerializer


# ✅ Liste et création des réalisations
@swagger_auto_schema(method='post', request_body=RealisationSerializer, responses={201: RealisationSerializer})
@api_view(['GET', 'POST'])
def realisation_list(request):
    if request.method == 'GET':
        realisations = Realisation.objects.all()

        # 🔍 filtres optionnels
        id_rapport = request.GET.get('id_rapport', None)
        if id_rapport is not None:
            realisations = realisations.filter(id_rapport=id_rapport)

        serializer = RealisationSerializer(realisations, many=True)
        return JsonResponse(
            {
                'success': True,
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = RealisationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(
                {
                    'success': True,
                    'data': serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ✅ Détail, mise à jour et suppression d’une réalisation
@swagger_auto_schema(method='put', request_body=RealisationSerializer, operation_description="Met à jour une réalisation")
@swagger_auto_schema(method='delete', operation_description="Supprime une réalisation par ID")
@api_view(['GET', 'PUT', 'DELETE'])
def realisation_detail(request, pk):
    try:
        realisation = Realisation.objects.get(pk=pk)
    except Realisation.DoesNotExist:
        return JsonResponse({'message': 'Réalisation non trouvée'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = RealisationSerializer(realisation)
        return JsonResponse(
            {
                'success': True,
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = RealisationSerializer(realisation, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(
                {
                    'success': True,
                    'data': serializer.data
                },
                status=status.HTTP_200_OK
            )
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        realisation.delete()
        return JsonResponse({'message': 'Réalisation supprimée avec succès !'}, status=status.HTTP_204_NO_CONTENT)
