from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser  # type: ignore
from rest_framework import status  # type: ignore
from rest_framework.decorators import api_view  # type: ignore
from drf_yasg.utils import swagger_auto_schema

from .models import EntiteProjet
from entitesprojets.serializers import EntiteProjetSerializer


# ✅ Liste et création des liaisons Entité-Projet
@swagger_auto_schema(method='post', request_body=EntiteProjetSerializer, responses={201: EntiteProjetSerializer})
@api_view(['GET', 'POST'])
def entite_projet_list(request):
    if request.method == 'GET':
        entite_projets = EntiteProjet.objects.all()

        # Filtre optionnel : id_entite ou id_projet
        id_entite = request.GET.get('id_entite', None)
        id_projet = request.GET.get('id_projet', None)

        if id_entite is not None:
            entite_projets = entite_projets.filter(id_entite=id_entite)
        if id_projet is not None:
            entite_projets = entite_projets.filter(id_projet=id_projet)

        serializer = EntiteProjetSerializer(entite_projets, many=True)
        return JsonResponse(
            {
                'success': True,
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = EntiteProjetSerializer(data=data)
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


# ✅ Récupération, mise à jour et suppression d’une liaison spécifique
@swagger_auto_schema(method='put', request_body=EntiteProjetSerializer, operation_description="Met à jour une relation Entité-Projet")
@swagger_auto_schema(method='delete', operation_description="Supprime une relation Entité-Projet par ID")
@api_view(['GET', 'PUT', 'DELETE'])
def entite_projet_detail(request, pk):
    try:
        entite_projet = EntiteProjet.objects.get(pk=pk)
    except EntiteProjet.DoesNotExist:
        return JsonResponse({'message': 'Relation Entité-Projet non trouvée'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = EntiteProjetSerializer(entite_projet)
        return JsonResponse(
            {
                'success': True,
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = EntiteProjetSerializer(entite_projet, data=data)
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
        entite_projet.delete()
        return JsonResponse({'message': 'Relation supprimée avec succès !'}, status=status.HTTP_204_NO_CONTENT)
