from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser  # type: ignore
from rest_framework import status  # type: ignore
from rest_framework.decorators import api_view  # type: ignore
from drf_yasg.utils import swagger_auto_schema

from projets.models import Projet
from .serializers import ProjetSerializer


# ✅ Liste et création des projets
@swagger_auto_schema(method='post', request_body=ProjetSerializer, responses={201: ProjetSerializer})
@api_view(['GET', 'POST'])
def projet_list(request):
    if request.method == 'GET':
        projets = Projet.objects.all()

        # 🔍 Filtres optionnels
        titre = request.GET.get('titre', None)
        statut = request.GET.get('statut', None)

        if titre is not None:
            projets = projets.filter(titre__icontains=titre)
        if statut is not None:
            projets = projets.filter(statut__icontains=statut)

        serializer = ProjetSerializer(projets, many=True)
        return JsonResponse(
            {
                'success': True,
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ProjetSerializer(data=data)
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


# ✅ Détail, mise à jour et suppression d’un projet
@swagger_auto_schema(method='put', request_body=ProjetSerializer, operation_description="Met à jour un projet")
@swagger_auto_schema(method='delete', operation_description="Supprime un projet par ID")
@api_view(['GET', 'PUT', 'DELETE'])
def projet_detail(request, pk):
    try:
        projet = Projet.objects.get(pk=pk)
    except Projet.DoesNotExist:
        return JsonResponse({'message': 'Projet non trouvé'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProjetSerializer(projet)
        return JsonResponse(
            {
                'success': True,
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = ProjetSerializer(projet, data=data)
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
        projet.delete()
        return JsonResponse({'message': 'Projet supprimé avec succès !'}, status=status.HTTP_204_NO_CONTENT)
