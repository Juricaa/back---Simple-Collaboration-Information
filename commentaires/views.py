from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser  # type: ignore
from rest_framework import status  # type: ignore
from rest_framework.decorators import api_view  # type: ignore
from drf_yasg.utils import swagger_auto_schema

from commentaires.models import Commentaire
from .serializers import CommentaireSerializer


# ✅ Liste et création des commentaires
@swagger_auto_schema(method='post', request_body=CommentaireSerializer, responses={201: CommentaireSerializer})
@api_view(['GET', 'POST'])
def commentaire_list(request):
    if request.method == 'GET':
        commentaires = Commentaire.objects.all()

        # 🔍 filtres optionnels
        id_projet = request.GET.get('id_projet', None)
        id_utilisateur = request.GET.get('id_utilisateur', None)
        etat = request.GET.get('etat', None)

        if id_projet is not None:
            commentaires = commentaires.filter(id_projet=id_projet)
        if id_utilisateur is not None:
            commentaires = commentaires.filter(id_utilisateur=id_utilisateur)
        if etat is not None:
            commentaires = commentaires.filter(etat__icontains=etat)

        serializer = CommentaireSerializer(commentaires, many=True)
        return JsonResponse(
            {
                'success': True,
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = CommentaireSerializer(data=data)
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


# ✅ Détail, mise à jour et suppression d’un commentaire
@swagger_auto_schema(method='put', request_body=CommentaireSerializer, operation_description="Met à jour un commentaire")
@swagger_auto_schema(method='delete', operation_description="Supprime un commentaire par ID")
@api_view(['GET', 'PUT', 'DELETE'])
def commentaire_detail(request, pk):
    try:
        commentaire = Commentaire.objects.get(pk=pk)
    except Commentaire.DoesNotExist:
        return JsonResponse({'message': 'Commentaire non trouvé'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CommentaireSerializer(commentaire)
        return JsonResponse(
            {
                'success': True,
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = CommentaireSerializer(commentaire, data=data)
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
        commentaire.delete()
        return JsonResponse({'message': 'Commentaire supprimé avec succès !'}, status=status.HTTP_204_NO_CONTENT)
