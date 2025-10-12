from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser  # type: ignore
from rest_framework import status  # type: ignore
from rest_framework.decorators import api_view  # type: ignore
from drf_yasg.utils import swagger_auto_schema

from rapports.models import Rapport
from .serializers import RapportSerializer



@swagger_auto_schema(method='post', request_body=RapportSerializer, responses={201: RapportSerializer})
@api_view(['GET', 'POST'])
def rapport_list(request):
    if request.method == 'GET':
        rapports = Rapport.objects.all()

  
        id_projet = request.GET.get('id_projet', None)
        periodicite = request.GET.get('periodicite', None)
        statut = request.GET.get('statut', None)

        if id_projet is not None:
            rapports = rapports.filter(id_projet=id_projet)
        if periodicite is not None:
            rapports = rapports.filter(periodicite=periodicite)
        if statut is not None:
            rapports = rapports.filter(statut__icontains=statut)

        serializer = RapportSerializer(rapports, many=True)
        return JsonResponse(
            {
                'success': True,
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = RapportSerializer(data=data)
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


@swagger_auto_schema(method='put', request_body=RapportSerializer, operation_description="Met à jour un rapport")
@swagger_auto_schema(method='delete', operation_description="Supprime un rapport par ID")
@api_view(['GET', 'PUT', 'DELETE'])
def rapport_detail(request, pk):
    try:
        rapport = Rapport.objects.get(pk=pk)
    except Rapport.DoesNotExist:
        return JsonResponse({'message': 'Rapport non trouvé'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = RapportSerializer(rapport)
        return JsonResponse(
            {
                'success': True,
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = RapportSerializer(rapport, data=data)
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
        rapport.delete()
        return JsonResponse({'message': 'Rapport supprimé avec succès !'}, status=status.HTTP_204_NO_CONTENT)
